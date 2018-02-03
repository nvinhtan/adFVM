
def List(*args):
    return list(args)

def expression(r, u1, u2, u3, p, gradr, gradu1, gradu2, gradu3, gradp, g, zero):
    rx1,rx2,rx3 = gradr.T
    u1x1,u1x2,u1x3 = gradu1.T
    u2x1,u2x2,u2x3 = gradu2.T
    u3x1,u3x2,u3x3 = gradu3.T
    px1,px2,px3 = gradp.T
    return List(List(zero,zero,zero,zero,zero),List(zero,p*((-3+g)*u1x1+(-1+g)*(u2x2+u3x3)),
-(p*(u1x2+u2x1)),-(p*(u1x3+u3x1)),
(p*(g**2*r**2*u1*(u1x1+u2x2+u3x3)+
r**2*(u1x2*u2+u2*u2x1+u1x3*u3+u3*u3x1+
u1*(3*u1x1+u2x2+u3x3))-
g*(px1*r-p*rx1+r**2*
(u1x2*u2+u2*u2x1+u1x3*u3+u3*u3x1+
2*u1*(2*u1x1+u2x2+u3x3)))))/((-1+g)*r**2)),
List(zero,-(p*(u1x2+u2x1)),g*p*(u1x1+u2x2+u3x3)-
p*(u1x1+3*u2x2+u3x3),-(p*(u2x3+u3x2)),
(p*(g**2*r**2*u2*(u1x1+u2x2+u3x3)+
r**2*(u1x1*u2+u1*(u1x2+u2x1)+3*u2*u2x2+u2x3*u3+u3*u3x2+
u2*u3x3)-g*(px2*r-p*rx2+
r**2*(2*u1x1*u2+u1*(u1x2+u2x1)+4*u2*u2x2+u2x3*u3+
u3*u3x2+2*u2*u3x3))))/((-1+g)*r**2)),
List(zero,-(p*(u1x3+u3x1)),-(p*(u2x3+u3x2)),
g*p*(u1x1+u2x2+u3x3)-p*(u1x1+u2x2+3*u3x3),
(p*(g**2*r**2*u3*(u1x1+u2x2+u3x3)+
r**2*(u1*(u1x3+u3x1)+u2*(u2x3+u3x2)+
u3*(u1x1+u2x2+3*u3x3))-
g*(px3*r-p*rx3+r**2*
(u1*(u1x3+u3x1)+u2*(u2x3+u3x2)+2*u3*(u1x1+u2x2+2*u3x3))
)))/((-1+g)*r**2)),
List(zero,(p*(g**2*r**2*u1*(u1x1+u2x2+u3x3)+
r**2*(u1x2*u2+u2*u2x1+u1x3*u3+u3*u3x1+
u1*(3*u1x1+u2x2+u3x3))-
g*(px1*r-p*rx1+r**2*
(u1x2*u2+u2*u2x1+u1x3*u3+u3*u3x1+
2*u1*(2*u1x1+u2x2+u3x3)))))/((-1+g)*r**2),
(p*(g**2*r**2*u2*(u1x1+u2x2+u3x3)+
r**2*(u1x1*u2+u1*(u1x2+u2x1)+3*u2*u2x2+u2x3*u3+u3*u3x2+
u2*u3x3)-g*(px2*r-p*rx2+
r**2*(2*u1x1*u2+u1*(u1x2+u2x1)+4*u2*u2x2+u2x3*u3+
u3*u3x2+2*u2*u3x3))))/((-1+g)*r**2),
(p*(g**2*r**2*u3*(u1x1+u2x2+u3x3)+
r**2*(u1*(u1x3+u3x1)+u2*(u2x3+u3x2)+
u3*(u1x1+u2x2+3*u3x3))-
g*(px3*r-p*rx3+r**2*
(u1*(u1x3+u3x1)+u2*(u2x3+u3x2)+2*u3*(u1x1+u2x2+2*u3x3))
)))/((-1+g)*r**2),
(p*(g**2*r**2*(u1**2+u2**2+u3**2)*(u1x1+u2x2+u3x3)+
r**2*(3*u2**2*u2x2+2*u2*u2x3*u3+u2x2*u3**2+
u1x1*(u2**2+u3**2)+
2*u1*(u1x2*u2+u2*u2x1+u3*(u1x3+u3x1))+2*u2*u3*u3x2+
u2**2*u3x3+3*u3**2*u3x3+u1**2*(3*u1x1+u2x2+u3x3))-
2*g*(px1*r*u1-p*(rx1*u1+rx2*u2+rx3*u3)+
r*(px2*u2+px3*u3+
r*(2*u2**2*u2x2+u2*u2x3*u3+u2x2*u3**2+
u1x1*(u2**2+u3**2)+
u1*(u1x2*u2+u2*u2x1+u3*(u1x3+u3x1))+u2*u3*u3x2+
u2**2*u3x3+2*u3**2*u3x3+u1**2*(2*u1x1+u2x2+u3x3))))))/
((-1+g)*r**2)))
    #return List(List(zero,zero,zero,zero,zero),List(zero,p*((-3 + g)*u1x1 + (-1 + g)*(u2x2 + u3x3)),    -(p*(u1x2 + u2x1)),-(p*(u1x3 + u3x1)),    (p*(g**2*r**2*u1*(u1x1 + u2x2 + u3x3) +          r**2*(u1x2*u2 + u2*u2x1 + u1x3*u3 + u3*u3x1 +             u1*(3*u1x1 + u2x2 + u3x3)) -          g*(px1*r - p*rx1 + r**2*             (u1x2*u2 + u2*u2x1 + u1x3*u3 + u3*u3x1 +                2*u1*(2*u1x1 + u2x2 + u3x3)))))/((-1 + g)*r**2)),   List(zero,-(p*(u1x2 + u2x1)),g*p*(u1x1 + u2x2 + u3x3) -      p*(u1x1 + 3*u2x2 + u3x3),-(p*(u2x3 + u3x2)),    (p*(g**2*r**2*u2*(u1x1 + u2x2 + u3x3) +          r**2*(u1x1*u2 + u1*(u1x2 + u2x1) + 3*u2*u2x2 + u2x3*u3 + u3*u3x2 +             u2*u3x3) - g*(px2*r - p*rx2 +             r**2*(2*u1x1*u2 + u1*(u1x2 + u2x1) + 4*u2*u2x2 + u2x3*u3 +                u3*u3x2 + 2*u2*u3x3))))/((-1 + g)*r**2)),   List(zero,-(p*(u1x3 + u3x1)),-(p*(u2x3 + u3x2)),    g*p*(u1x1 + u2x2 + u3x3) - p*(u1x1 + u2x2 + 3*u3x3),    (p*(g**2*r**2*u3*(u1x1 + u2x2 + u3x3) +          r**2*(u1*(u1x3 + u3x1) + u2*(u2x3 + u3x2) +             u3*(u1x1 + u2x2 + 3*u3x3)) -          g*(px3*r - p*rx3 + r**2*             (u1*(u1x3 + u3x1) + u2*(u2x3 + u3x2) + 2*u3*(u1x1 + u2x2 + 2*u3x3))            )))/((-1 + g)*r**2)),   List(zero,(p*(g**2*r**2*u1*(u1x1 + u2x2 + u3x3) +          r**2*(u1x2*u2 + u2*u2x1 + u1x3*u3 + u3*u3x1 +             u1*(3*u1x1 + u2x2 + u3x3)) -          g*(px1*r - p*rx1 + r**2*             (u1x2*u2 + u2*u2x1 + u1x3*u3 + u3*u3x1 +                2*u1*(2*u1x1 + u2x2 + u3x3)))))/((-1 + g)*r**2),    (p*(g**2*r**2*u2*(u1x1 + u2x2 + u3x3) +          r**2*(u1x1*u2 + u1*(u1x2 + u2x1) + 3*u2*u2x2 + u2x3*u3 + u3*u3x2 +             u2*u3x3) - g*(px2*r - p*rx2 +             r**2*(2*u1x1*u2 + u1*(u1x2 + u2x1) + 4*u2*u2x2 + u2x3*u3 +                u3*u3x2 + 2*u2*u3x3))))/((-1 + g)*r**2),    (p*(g**2*r**2*u3*(u1x1 + u2x2 + u3x3) +          r**2*(u1*(u1x3 + u3x1) + u2*(u2x3 + u3x2) +             u3*(u1x1 + u2x2 + 3*u3x3)) -          g*(px3*r - p*rx3 + r**2*             (u1*(u1x3 + u3x1) + u2*(u2x3 + u3x2) + 2*u3*(u1x1 + u2x2 + 2*u3x3))            )))/((-1 + g)*r**2),    (p*(g**2*r**2*(u1**2 + u2**2 + u3**2)*(u1x1 + u2x2 + u3x3) +          r**2*(3*u2**2*u2x2 + 2*u2*u2x3*u3 + u2x2*u3**2 +             u1x1*(u2**2 + u3**2) +             2*u1*(u1x2*u2 + u2*u2x1 + u3*(u1x3 + u3x1)) + 2*u2*u3*u3x2 +             u2**2*u3x3 + 3*u3**2*u3x3 + u1**2*(3*u1x1 + u2x2 + u3x3)) -          2*g*(px1*r*u1 - p*(rx1*u1 + rx2*u2 + rx3*u3) +             r*(px2*u2 + px3*u3 +                r*(2*u2**2*u2x2 + u2*u2x3*u3 + u2x2*u3**2 +                   u1x1*(u2**2 + u3**2) +                   u1*(u1x2*u2 + u2*u2x1 + u3*(u1x3 + u3x1)) + u2*u3*u3x2 +                   u2**2*u3x3 + 2*u3**2*u3x3 + u1**2*(2*u1x1 + u2x2 + u3x3))))))/     ((-1 + g)*r**2)))

def expression_code(r, U, p, gradrho, gradU, gradp, g, zero):
    u1, u2, u3 = U[0], U[1], U[2]
    rx1,rx2,rx3 = gradrho[0], gradrho[1], gradrho[2]
    u1x1,u1x2,u1x3 = gradU[0,0], gradU[0,1], gradU[0, 2]
    u2x1,u2x2,u2x3 = gradU[1,0], gradU[1,1], gradU[1,2]
    u3x1,u3x2,u3x3 = gradU[2, 0], gradU[2,1], gradU[2,2]
    px1,px2,px3 = gradp[0], gradp[1], gradp[2]
    return List(List(zero,zero,zero,zero,zero),List(zero,p*((-3 + g)*u1x1 + (-1 + g)*(u2x2 + u3x3)),    -(p*(u1x2 + u2x1)),-(p*(u1x3 + u3x1)),    (p*(g**2*r**2*u1*(u1x1 + u2x2 + u3x3) +          r**2*(u1x2*u2 + u2*u2x1 + u1x3*u3 + u3*u3x1 +             u1*(3*u1x1 + u2x2 + u3x3)) -          g*(px1*r - p*rx1 + r**2*             (u1x2*u2 + u2*u2x1 + u1x3*u3 + u3*u3x1 +                2*u1*(2*u1x1 + u2x2 + u3x3)))))/((-1 + g)*r**2)),   List(zero,-(p*(u1x2 + u2x1)),g*p*(u1x1 + u2x2 + u3x3) -      p*(u1x1 + 3*u2x2 + u3x3),-(p*(u2x3 + u3x2)),    (p*(g**2*r**2*u2*(u1x1 + u2x2 + u3x3) +          r**2*(u1x1*u2 + u1*(u1x2 + u2x1) + 3*u2*u2x2 + u2x3*u3 + u3*u3x2 +             u2*u3x3) - g*(px2*r - p*rx2 +             r**2*(2*u1x1*u2 + u1*(u1x2 + u2x1) + 4*u2*u2x2 + u2x3*u3 +                u3*u3x2 + 2*u2*u3x3))))/((-1 + g)*r**2)),   List(zero,-(p*(u1x3 + u3x1)),-(p*(u2x3 + u3x2)),    g*p*(u1x1 + u2x2 + u3x3) - p*(u1x1 + u2x2 + 3*u3x3),    (p*(g**2*r**2*u3*(u1x1 + u2x2 + u3x3) +          r**2*(u1*(u1x3 + u3x1) + u2*(u2x3 + u3x2) +             u3*(u1x1 + u2x2 + 3*u3x3)) -          g*(px3*r - p*rx3 + r**2*             (u1*(u1x3 + u3x1) + u2*(u2x3 + u3x2) + 2*u3*(u1x1 + u2x2 + 2*u3x3))            )))/((-1 + g)*r**2)),   List(zero,(p*(g**2*r**2*u1*(u1x1 + u2x2 + u3x3) +          r**2*(u1x2*u2 + u2*u2x1 + u1x3*u3 + u3*u3x1 +             u1*(3*u1x1 + u2x2 + u3x3)) -          g*(px1*r - p*rx1 + r**2*             (u1x2*u2 + u2*u2x1 + u1x3*u3 + u3*u3x1 +                2*u1*(2*u1x1 + u2x2 + u3x3)))))/((-1 + g)*r**2),    (p*(g**2*r**2*u2*(u1x1 + u2x2 + u3x3) +          r**2*(u1x1*u2 + u1*(u1x2 + u2x1) + 3*u2*u2x2 + u2x3*u3 + u3*u3x2 +             u2*u3x3) - g*(px2*r - p*rx2 +             r**2*(2*u1x1*u2 + u1*(u1x2 + u2x1) + 4*u2*u2x2 + u2x3*u3 +                u3*u3x2 + 2*u2*u3x3))))/((-1 + g)*r**2),    (p*(g**2*r**2*u3*(u1x1 + u2x2 + u3x3) +          r**2*(u1*(u1x3 + u3x1) + u2*(u2x3 + u3x2) +             u3*(u1x1 + u2x2 + 3*u3x3)) -          g*(px3*r - p*rx3 + r**2*             (u1*(u1x3 + u3x1) + u2*(u2x3 + u3x2) + 2*u3*(u1x1 + u2x2 + 2*u3x3))            )))/((-1 + g)*r**2),    (p*(g**2*r**2*(u1**2 + u2**2 + u3**2)*(u1x1 + u2x2 + u3x3) +          r**2*(3*u2**2*u2x2 + 2*u2*u2x3*u3 + u2x2*u3**2 +             u1x1*(u2**2 + u3**2) +             2*u1*(u1x2*u2 + u2*u2x1 + u3*(u1x3 + u3x1)) + 2*u2*u3*u3x2 +             u2**2*u3x3 + 3*u3**2*u3x3 + u1**2*(3*u1x1 + u2x2 + u3x3)) -          2*g*(px1*r*u1 - p*(rx1*u1 + rx2*u2 + rx3*u3) +             r*(px2*u2 + px3*u3 +                r*(2*u2**2*u2x2 + u2*u2x3*u3 + u2x2*u3**2 +                   u1x1*(u2**2 + u3**2) +                   u1*(u1x2*u2 + u2*u2x1 + u3*(u1x3 + u3x1)) + u2*u3*u3x2 +                   u2**2*u3x3 + 2*u3**2*u3x3 + u1**2*(2*u1x1 + u2x2 + u3x3))))))/     ((-1 + g)*r**2)))
