
import numpy as np
def expression(r, ru1, ru2, ru3, rE, g, one, zero):
    return [one, zero, zero, zero, zero, zero, one, zero, zero, zero, zero, zero, one, zero, zero, zero, zero, zero, one, zero, zero, zero, zero, zero, one, zero, one, zero, zero, zero, -ru1**2/r**2, 2*ru1/r, zero, zero, zero, -ru1*ru2/r**2, ru2/r, ru1/r, zero, zero, -ru1*ru3/r**2, ru3/r, zero, ru1/r, zero, ru1*(g*r*rE + g*(-2*r*rE + ru1**2 + ru2**2 + ru3**2) - ru1**2 - ru2**2 - ru3**2)/r**3, (-g*(-2*r*rE + ru1**2 + ru2**2 + ru3**2) - 2*ru1**2*(g - 1) + ru1**2 + ru2**2 + ru3**2)/(2*r**2), -ru1*ru2*(g - 1)/r**2, -ru1*ru3*(g - 1)/r**2, g*ru1/r, zero, zero, one, zero, zero, -ru1*ru2/r**2, ru2/r, ru1/r, zero, zero, -ru2**2/r**2, zero, 2*ru2/r, zero, zero, -ru2*ru3/r**2, zero, ru3/r, ru2/r, zero, ru2*(g*r*rE + g*(-2*r*rE + ru1**2 + ru2**2 + ru3**2) - ru1**2 - ru2**2 - ru3**2)/r**3, -ru1*ru2*(g - 1)/r**2, (-g*(-2*r*rE + ru1**2 + ru2**2 + ru3**2) + ru1**2 - 2*ru2**2*(g - 1) + ru2**2 + ru3**2)/(2*r**2), -ru2*ru3*(g - 1)/r**2, g*ru2/r, zero, zero, zero, one, zero, -ru1*ru3/r**2, ru3/r, zero, ru1/r, zero, -ru2*ru3/r**2, zero, ru3/r, ru2/r, zero, -ru3**2/r**2, zero, zero, 2*ru3/r, zero, ru3*(g*r*rE + g*(-2*r*rE + ru1**2 + ru2**2 + ru3**2) - ru1**2 - ru2**2 - ru3**2)/r**3, -ru1*ru3*(g - 1)/r**2, -ru2*ru3*(g - 1)/r**2, (-g*(-2*r*rE + ru1**2 + ru2**2 + ru3**2) + ru1**2 + ru2**2 - 2*ru3**2*(g - 1) + ru3**2)/(2*r**2), g*ru3/r, zero, zero, zero, zero, one, ru1*(g*r*rE + g*(-2*r*rE + ru1**2 + ru2**2 + ru3**2) - ru1**2 - ru2**2 - ru3**2)/r**3, (-g*(-2*r*rE + ru1**2 + ru2**2 + ru3**2) - 2*ru1**2*(g - 1) + ru1**2 + ru2**2 + ru3**2)/(2*r**2), -ru1*ru2*(g - 1)/r**2, -ru1*ru3*(g - 1)/r**2, g*ru1/r, ru2*(g*r*rE + g*(-2*r*rE + ru1**2 + ru2**2 + ru3**2) - ru1**2 - ru2**2 - ru3**2)/r**3, -ru1*ru2*(g - 1)/r**2, (-g*(-2*r*rE + ru1**2 + ru2**2 + ru3**2) + ru1**2 - 2*ru2**2*(g - 1) + ru2**2 + ru3**2)/(2*r**2), -ru2*ru3*(g - 1)/r**2, g*ru2/r, ru3*(g*r*rE + g*(-2*r*rE + ru1**2 + ru2**2 + ru3**2) - ru1**2 - ru2**2 - ru3**2)/r**3, -ru1*ru3*(g - 1)/r**2, -ru2*ru3*(g - 1)/r**2, (-g*(-2*r*rE + ru1**2 + ru2**2 + ru3**2) + ru1**2 + ru2**2 - 2*ru3**2*(g - 1) + ru3**2)/(2*r**2), g*ru3/r, -(4*g*r**2*rE**2 - 3*g*ru1**4 - 6*g*ru1**2*ru2**2 - 6*g*ru1**2*ru3**2 - 3*g*ru2**4 - 6*g*ru2**2*ru3**2 - 3*g*ru3**4 + 3*ru1**4 + 6*ru1**2*ru2**2 + 6*ru1**2*ru3**2 + 3*ru2**4 + 6*ru2**2*ru3**2 + 3*ru3**4)/(4*r**4), -ru1*(g - 1)*(ru1**2 + ru2**2 + ru3**2)/r**3, -ru2*(g - 1)*(ru1**2 + ru2**2 + ru3**2)/r**3, -ru3*(g - 1)*(ru1**2 + ru2**2 + ru3**2)/r**3, 2*g*rE/r],             [zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, (2*ru1**2 - (g - 1)*(ru1**2 + ru2**2 + ru3**2))/r**3, ru1*(g - 3)/r**2, ru2*(g - 1)/r**2, ru3*(g - 1)/r**2, zero, ru1*(g - 3)/r**2, (-g + 3)/r, zero, zero, zero, ru2*(g - 1)/r**2, zero, (-g + 1)/r, zero, zero, ru3*(g - 1)/r**2, zero, zero, (-g + 1)/r, zero, zero, zero, zero, zero, zero, 2*ru1*ru2/r**3, -ru2/r**2, -ru1/r**2, zero, zero, -ru2/r**2, zero, 1/r, zero, zero, -ru1/r**2, 1/r, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, 2*ru1*ru3/r**3, -ru3/r**2, zero, -ru1/r**2, zero, -ru3/r**2, zero, zero, 1/r, zero, zero, zero, zero, zero, zero, -ru1/r**2, 1/r, zero, zero, zero, zero, zero, zero, zero, zero, 2*ru1*ru2/r**3, -ru2/r**2, -ru1/r**2, zero, zero, -ru2/r**2, zero, 1/r, zero, zero, -ru1/r**2, 1/r, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, (2*ru2**2 - (g - 1)*(ru1**2 + ru2**2 + ru3**2))/r**3, ru1*(g - 1)/r**2, ru2*(g - 3)/r**2, ru3*(g - 1)/r**2, zero, ru1*(g - 1)/r**2, (-g + 1)/r, zero, zero, zero, ru2*(g - 3)/r**2, zero, (-g + 3)/r, zero, zero, ru3*(g - 1)/r**2, zero, zero, (-g + 1)/r, zero, zero, zero, zero, zero, zero, 2*ru2*ru3/r**3, zero, -ru3/r**2, -ru2/r**2, zero, zero, zero, zero, zero, zero, -ru3/r**2, zero, zero, 1/r, zero, -ru2/r**2, zero, 1/r, zero, zero, zero, zero, zero, zero, zero, 2*ru1*ru3/r**3, -ru3/r**2, zero, -ru1/r**2, zero, -ru3/r**2, zero, zero, 1/r, zero, zero, zero, zero, zero, zero, -ru1/r**2, 1/r, zero, zero, zero, zero, zero, zero, zero, zero, 2*ru2*ru3/r**3, zero, -ru3/r**2, -ru2/r**2, zero, zero, zero, zero, zero, zero, -ru3/r**2, zero, zero, 1/r, zero, -ru2/r**2, zero, 1/r, zero, zero, zero, zero, zero, zero, zero, (2*ru3**2 - (g - 1)*(ru1**2 + ru2**2 + ru3**2))/r**3, ru1*(g - 1)/r**2, ru2*(g - 1)/r**2, ru3*(g - 3)/r**2, zero, ru1*(g - 1)/r**2, (-g + 1)/r, zero, zero, zero, ru2*(g - 1)/r**2, zero, (-g + 1)/r, zero, zero, ru3*(g - 3)/r**2, zero, zero, (-g + 3)/r, zero, zero, zero, zero, zero, zero, ru1*(2*g*r*rE - 3*g*ru1**2 - 3*g*ru2**2 - 3*g*ru3**2 + 3*ru1**2 + 3*ru2**2 + 3*ru3**2)/r**4, (-g*r*rE + 3*g*ru1**2 + g*ru2**2 + g*ru3**2 - 3*ru1**2 - ru2**2 - ru3**2)/r**3, 2*ru1*ru2*(g - 1)/r**3, 2*ru1*ru3*(g - 1)/r**3, -g*ru1/r**2, (-g*r*rE + 3*g*ru1**2 + g*ru2**2 + g*ru3**2 - 3*ru1**2 - ru2**2 - ru3**2)/r**3, -3*ru1*(g - 1)/r**2, -ru2*(g - 1)/r**2, -ru3*(g - 1)/r**2, g/r, 2*ru1*ru2*(g - 1)/r**3, -ru2*(g - 1)/r**2, -ru1*(g - 1)/r**2, zero, zero, 2*ru1*ru3*(g - 1)/r**3, -ru3*(g - 1)/r**2, zero, -ru1*(g - 1)/r**2, zero, -g*ru1/r**2, g/r, zero, zero, zero, ru2*(2*g*r*rE - 3*g*ru1**2 - 3*g*ru2**2 - 3*g*ru3**2 + 3*ru1**2 + 3*ru2**2 + 3*ru3**2)/r**4, 2*ru1*ru2*(g - 1)/r**3, (-g*r*rE + g*ru1**2 + 3*g*ru2**2 + g*ru3**2 - ru1**2 - 3*ru2**2 - ru3**2)/r**3, 2*ru2*ru3*(g - 1)/r**3, -g*ru2/r**2, 2*ru1*ru2*(g - 1)/r**3, -ru2*(g - 1)/r**2, -ru1*(g - 1)/r**2, zero, zero, (-g*r*rE + g*ru1**2 + 3*g*ru2**2 + g*ru3**2 - ru1**2 - 3*ru2**2 - ru3**2)/r**3, -ru1*(g - 1)/r**2, -3*ru2*(g - 1)/r**2, -ru3*(g - 1)/r**2, g/r, 2*ru2*ru3*(g - 1)/r**3, zero, -ru3*(g - 1)/r**2, -ru2*(g - 1)/r**2, zero, -g*ru2/r**2, zero, g/r, zero, zero, ru3*(2*g*r*rE - 3*g*ru1**2 - 3*g*ru2**2 - 3*g*ru3**2 + 3*ru1**2 + 3*ru2**2 + 3*ru3**2)/r**4, 2*ru1*ru3*(g - 1)/r**3, 2*ru2*ru3*(g - 1)/r**3, (-g*r*rE + g*ru1**2 + g*ru2**2 + 3*g*ru3**2 - ru1**2 - ru2**2 - 3*ru3**2)/r**3, -g*ru3/r**2, 2*ru1*ru3*(g - 1)/r**3, -ru3*(g - 1)/r**2, zero, -ru1*(g - 1)/r**2, zero, 2*ru2*ru3*(g - 1)/r**3, zero, -ru3*(g - 1)/r**2, -ru2*(g - 1)/r**2, zero, (-g*r*rE + g*ru1**2 + g*ru2**2 + 3*g*ru3**2 - ru1**2 - ru2**2 - 3*ru3**2)/r**3, -ru1*(g - 1)/r**2, -ru2*(g - 1)/r**2, -3*ru3*(g - 1)/r**2, g/r, -g*ru3/r**2, zero, zero, g/r, zero],             [r, ru1, ru2, ru3, rE, ru1, ru1**2/r, ru1*ru2/r, ru1*ru3/r, ru1*(-g*(-2*r*rE + ru1**2 + ru2**2 + ru3**2) + ru1**2 + ru2**2 + ru3**2)/(2*r**2), ru2, ru1*ru2/r, ru2**2/r, ru2*ru3/r, ru2*(-g*(-2*r*rE + ru1**2 + ru2**2 + ru3**2) + ru1**2 + ru2**2 + ru3**2)/(2*r**2), ru3, ru1*ru3/r, ru2*ru3/r, ru3**2/r, ru3*(-g*(-2*r*rE + ru1**2 + ru2**2 + ru3**2) + ru1**2 + ru2**2 + ru3**2)/(2*r**2), rE, ru1*(-g*(-2*r*rE + ru1**2 + ru2**2 + ru3**2) + ru1**2 + ru2**2 + ru3**2)/(2*r**2), ru2*(-g*(-2*r*rE + ru1**2 + ru2**2 + ru3**2) + ru1**2 + ru2**2 + ru3**2)/(2*r**2), ru3*(-g*(-2*r*rE + ru1**2 + ru2**2 + ru3**2) + ru1**2 + ru2**2 + ru3**2)/(2*r**2), (-g*(g - 1)*(-2*r*rE + ru1**2 + ru2**2 + ru3**2)**2 + (-g*(-2*r*rE + ru1**2 + ru2**2 + ru3**2) + ru1**2 + ru2**2 + ru3**2)**2)/(4*r**3)],             [zero, one, zero, zero, zero, zero, zero, one, zero, zero, zero, zero, zero, one, zero, (-ru1**2 + (g - 1)*(ru1**2 + ru2**2 + ru3**2)/2)/r**2, ru1*(-g + 3)/r, -ru2*(g - 1)/r, -ru3*(g - 1)/r, g - 1, -ru1*ru2/r**2, ru2/r, ru1/r, zero, zero, -ru1*ru3/r**2, ru3/r, zero, ru1/r, zero, -ru1*ru2/r**2, ru2/r, ru1/r, zero, zero, (-ru2**2 + (g - 1)*(ru1**2 + ru2**2 + ru3**2)/2)/r**2, -ru1*(g - 1)/r, ru2*(-g + 3)/r, -ru3*(g - 1)/r, g - 1, -ru2*ru3/r**2, zero, ru3/r, ru2/r, zero, -ru1*ru3/r**2, ru3/r, zero, ru1/r, zero, -ru2*ru3/r**2, zero, ru3/r, ru2/r, zero, (-ru3**2 + (g - 1)*(ru1**2 + ru2**2 + ru3**2)/2)/r**2, -ru1*(g - 1)/r, -ru2*(g - 1)/r, ru3*(-g + 3)/r, g - 1, -ru1*(g*r*rE - g*ru1**2 - g*ru2**2 - g*ru3**2 + ru1**2 + ru2**2 + ru3**2)/r**3, (2*r*rE + 2*ru1**2*(-g + 1) - (g - 1)*(-2*r*rE + ru1**2 + ru2**2 + ru3**2))/(2*r**2), -ru1*ru2*(g - 1)/r**2, -ru1*ru3*(g - 1)/r**2, g*ru1/r, -ru2*(g*r*rE - g*ru1**2 - g*ru2**2 - g*ru3**2 + ru1**2 + ru2**2 + ru3**2)/r**3, -ru1*ru2*(g - 1)/r**2, (2*r*rE + 2*ru2**2*(-g + 1) - (g - 1)*(-2*r*rE + ru1**2 + ru2**2 + ru3**2))/(2*r**2), -ru2*ru3*(g - 1)/r**2, g*ru2/r, -ru3*(g*r*rE - g*ru1**2 - g*ru2**2 - g*ru3**2 + ru1**2 + ru2**2 + ru3**2)/r**3, -ru1*ru3*(g - 1)/r**2, -ru2*ru3*(g - 1)/r**2, (2*r*rE + 2*ru3**2*(-g + 1) - (g - 1)*(-2*r*rE + ru1**2 + ru2**2 + ru3**2))/(2*r**2), g*ru3/r]
    