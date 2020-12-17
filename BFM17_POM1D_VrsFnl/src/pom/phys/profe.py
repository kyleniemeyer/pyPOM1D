# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# MODEL  POM - Princeton Ocean Model
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#
# # ROUTINE: Profe
#
# DESCRIPTION
#
#   This subroutine solves for vertical diffusivity
#
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
import numpy as np
from decimal import *


def PROFE(FF, WFSURF, FSURF, NBC, DT2):

    from BFM17_POM1D_VrsFnl.src.BFM.General.ModuleGlobalMem import RLEN
    from BFM17_POM1D_VrsFnl.src.pom.phys.POMModule import H, KB, A, C, L, DZ, DZZ, VH, VHP, Z, UMOL, KH

    getcontext().prec = 12  # 12-digit precision (ilong)

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    #   SCALAR ARGUMENTS
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # DT2, FSURF, WFSURF = Decimal()
    # NBC = Decimal()

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    #   ARRAY ARGUMENTS
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # FF = np.empty(KB,dtype=float)

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    #   LOCAL SCALARS
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    DH, UMOLPR = Decimal()
    K, KI = Decimal()

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    #   LOCAL ARRAYS
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    EXTC, TR = np.empty(5,dtype=float)
    RAD = np.empty(KB,dtype=float)

    UMOLPR = 1.e-5
    DH = H

    for K in range(1, KB - 1):
        A[K - 1] = -DT2 * (KH[K] + UMOLPR) / (DZ[K - 1] * DZZ[K - 1] * DH * DH)
        C[K] = -DT2 * (KH[K] + UMOLPR) / (DZ[K] * DZZ[K - 1] * DH * DH)

    #    GO TO (51,52) NBC
    #
    # 51 CONTINUE
        VH[0] = A[0] / (A[0]-1.)
        VHP[0] = -DT2 * WFSURF / (-DZ[0]*DH) - FF[0]
        VHP[0] = VHP[0] / (A[0]-1.)
    #    GO TO 53
    # 52 CONTINUE
        VH[0] = 0.
        VHP[0] = FSURF
    # 53 CONTINUE

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    #   THE FOLLOWING SECTION SOLVES THE EQUATION
    #   DT2*(KH*FF')' -FF = FB
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    for K in range(1, KB - 2):
        VHP[K] = 1. / (A[K] + C[K] * (1. - VH[K - 1]) - 1.)
        VH[K] = A[K] * VHP[K]
        VHP[K] = (C[K] * VHP[K - 1] - FF[K]) * VHP[K]

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    #   INSTEAD OF MATCHING SOLUTION TO A LOWER LAYER VALUE OF F(KB-1),
    #   ONE MAY IMPOSE AN ADIABATIC BOTTOM B.C. BY REMOVING C'S FROM
    #   C OL. 1 OF THE NEXT TWO LINES.
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    FF[KB - 2] = (C[KB - 2] * VHP[KB - 3] - FF[KB - 2]) / (C[KB - 2] * (1. - VH[KB - 1]) - 1.)
    # 99 CONTINUE
    for K in range(1, KB - 1):
        KI = KB - K
        FF[KI] = VH[KI] * FF[KI + 1] + VHP[KI]

    for K in range(0, KB):
        VH[K] = 0.0
        VHP[K] = 0.0
        A[K] = 0.0
        C[K] = 0.0

    return

# EOC
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#   MODEL  POM - Princeton Ocean Model
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=