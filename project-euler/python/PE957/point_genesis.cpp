//-------------------------------------------------------------
//  Point‑Genesis   –   Project Euler 957
//  g(n) for n ≤ 16   in well under sixty seconds
//-------------------------------------------------------------

#include <iostream>
#include <iomanip>
#include <array>
#include <unordered_set>
#include <vector>
#include <utility>
#include <stdexcept>
#include <boost/multiprecision/cpp_int.hpp>

using std::size_t;
using boost::multiprecision::cpp_int;

/* ---------------- exact rationals ---------------- */
struct Q{
    cpp_int n,d;
    Q(cpp_int nn=0, cpp_int dd=1){ set(nn,dd); }
    void set(cpp_int nn, cpp_int dd){
        if(dd<0){ nn=-nn; dd=-dd; }
        cpp_int g=gcd(nn<0?-nn:nn,dd);
        n=nn/g; d=dd/g;
    }
    static cpp_int gcd(cpp_int a, cpp_int b){
        while(b){ cpp_int t=a%b; a=b; b=t; }
        return a<0?-a:a;
    }
    friend bool operator==(Q const&a,Q const&b){ return a.n==b.n&&a.d==b.d; }
    friend bool operator!=(Q const&a,Q const&b){ return !(a==b); }
    friend Q operator+(Q const&a,Q const&b){ return Q(a.n*b.d+b.n*a.d,a.d*b.d);}
    friend Q operator-(Q const&a,Q const&b){ return Q(a.n*b.d-b.n*a.d,a.d*b.d);}
    friend Q operator*(Q const&a,Q const&b){ return Q(a.n*b.n,a.d*b.d); }
    friend Q operator/(Q const&a,Q const&b){ return Q(a.n*b.d,a.d*b.n); }
};

/* ---------------- fast hashing for cpp_int -------- */
inline std::size_t limb_hash(cpp_int const& x) noexcept{
    auto const& b=x.backend();
    std::size_t h=14695981039346656037ull;
    for(std::size_t i=0,n=b.size(); i<n; ++i){
        h=(h^static_cast<std::size_t>(b.limbs()[i]))*1099511628211ull;
    }
    return h;
}
struct QHasher{
    std::size_t operator()(Q const&q) const noexcept{
        return (limb_hash(q.n)<<1)^limb_hash(q.d);
    }
};

/* ---------------- points & slopes ----------------- */
struct Pt{ Q x,y; bool operator==(Pt const& other) const { return x==other.x && y==other.y; } };
struct PtHasher{
    std::size_t operator()(Pt const&p)const noexcept{
        return (QHasher()(p.x)<<1)^QHasher()(p.y);
    }
};
struct Sl{
    cpp_int dy,dx;                 // dx≥0 , gcd(|dy|,dx)=1 ; dx=0 ⇒ vertical
    Sl(cpp_int dy_=0, cpp_int dx_=1){ set(dy_,dx_); }
    Sl(Q dy_q, Q dx_q){            // from rationals
        if(dx_q.n==0){ dy=1; dx=0; return;}
        cpp_int num=dy_q.n*dx_q.d, den=dy_q.d*dx_q.n;
        set(num,den);
    }
    void set(cpp_int dy_, cpp_int dx_){
        if(dx_==0){ dy=1; dx=0; return;}
        if(dx_<0){ dy_=-dy_; dx_=-dx_;}
        cpp_int g=Q::gcd(dy_<0?-dy_:dy_,dx_);
        dy=dy_/g; dx=dx_/g;
    }
    bool operator==(Sl const&b)const{ return dy==b.dy&&dx==b.dx; }
};
struct SlHasher{
    std::size_t operator()(Sl const&s)const noexcept{
        return (limb_hash(s.dy)<<1)^limb_hash(s.dx);
    }
};

/* ---------------- helpers ------------------------- */
using USetPt=std::unordered_set<Pt,PtHasher>;
using USetSl=std::unordered_set<Sl,SlHasher>;

static Pt intersect(std::pair<int,int> R1, Sl const&s1,
                    std::pair<int,int> R2, Sl const&s2){
    bool v1=(s1.dx==0), v2=(s2.dx==0);
    if(v1&&v2) throw std::runtime_error("parallel");
    if(v1||v2){
        cpp_int x=v1?R1.first:R2.first;
        Sl s=v1?s2:s1; auto R=v1?R2:R1;
        Q X(x); Q Y=Q(R.second)+Q(s.dy,s.dx)*(X-Q(R.first));
        return {X,Y};
    }
    Q m1(s1.dy,s1.dx), m2(s2.dy,s2.dx);
    if(m1==m2) throw std::runtime_error("parallel slopes");
    cpp_int x1=R1.first,y1=R1.second,x2=R2.first,y2=R2.second;
    Q X=(m1*Q(x1)-m2*Q(x2)+Q(y2)-Q(y1))/(m1-m2);
    Q Y=m1*(X-Q(x1))+Q(y1);
    return {X,Y};
}

/* ---------------- main ---------------------------- */
int main(){
    const std::array<std::pair<int,int>,3> R={{{0,0},{7,0},{0,11}}};
    const Pt B0{Q(3),Q(2)}, B1{Q(5),Q(7)};
    constexpr int N=16;

    USetPt blues; blues.reserve(7'000'000u);
    blues.insert(B0); blues.insert(B1);

    std::array<USetSl,3> S;
    for(int i=0;i<3;++i)
        for(Pt const& B:{B0,B1})
            S[i].insert(Sl(B.y-Q(R[i].second), B.x-Q(R[i].first)));

    std::array<std::vector<Sl>,3> deltaS;
    for(int i=0;i<3;++i){
        deltaS[i].assign(S[i].begin(),S[i].end());
        S[i].reserve(S[i].size()*2);
    }

    std::cout<<"day 0 : |B| = "<<blues.size()<<'\n';

    for(int day=1; day<=N; ++day){
        std::array<std::vector<Sl>,3> nextDelta;
        USetPt deltaB; deltaB.reserve(1'000'000u);

        auto cart=[&](auto const&A,auto const&B,int i,int j,int k){
            for(auto const& si:A)
                for(auto const& sj:B){
                    if(si==sj) continue;
                    Pt P=intersect(R[i],si,R[j],sj);
                    if(blues.count(P) || !deltaB.insert(P).second) continue;
                    nextDelta[k].emplace_back(P.y-Q(R[k].second),
                                              P.x-Q(R[k].first));
                }
        };

        for(auto [i,j]: std::array<std::pair<int,int>,3>{{{0,1},{0,2},{1,2}}}){
            int k=3-i-j;
            cart(deltaS[i],S[j],i,j,k);   // new × old
            cart(S[i],deltaS[j],i,j,k);   // old × new
        }

        blues.insert(deltaB.begin(),deltaB.end());
        for(int i=0;i<3;++i){
            S[i].insert(nextDelta[i].begin(),nextDelta[i].end());
            deltaS[i].swap(nextDelta[i]);
        }

        std::cout<<"day "<<std::setw(2)<<day
                 <<" : |B| = "<<blues.size()
                 <<"   (new "<<deltaB.size()<<")\n";
    }
    std::cout<<"\nanswer  g("<<N<<") = "<<blues.size()<<'\n';
    return 0;
}
