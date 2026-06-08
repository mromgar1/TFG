from functools import partial

import gdsfactory as gf
from gdsfactory.typings import (
    CrossSectionSpec,
)

from gdsfactory.component import Component
from gdsfactory.typings import CrossSectionSpec, ComponentSpec
from gdsfactory.typings import LayerSpec, Size

from upvfab.sin300.cband.tech import LAYER, TECH

# building blocks

@gf.cell 
def b_symmetric_mmi(L_mmi=144.7, W_mmi=10, Aw = 0.72, L_wg=20, lt=50, wt=1.0, Wt=3, d_io=1.97, layer="WG"):

    c = gf.Component()
    W_narrow= W_mmi - Aw

    #vértices ( mismos que uso en la simulación de tidy)

    polys = {
        "mmi": [
            (0.0,         -W_mmi / 2),
            (L_mmi / 4,   -W_narrow / 2),
            (L_mmi / 2,   -W_mmi / 2),
            (3*L_mmi / 4, -W_narrow / 2),
            (L_mmi,       -W_mmi / 2),
            (L_mmi,        W_mmi / 2),
            (3*L_mmi / 4,  W_narrow / 2),
            (L_mmi / 2,    W_mmi / 2),
            (L_mmi / 4,    W_narrow / 2),
            (0.0,          W_mmi / 2),
        ],

        "in_bot_taper": [
            (-lt, -W_mmi / 2 + d_io + Wt / 2 - wt / 2),
            (0.0, -W_mmi / 2 + d_io),
            (0.0, -W_mmi / 2 + d_io + Wt),
            (-lt, -W_mmi / 2 + d_io + Wt / 2 + wt / 2),
        ],

        "in_top_taper": [
            (-lt, W_mmi / 2 - d_io - Wt / 2 - wt / 2),
            (0.0, W_mmi / 2 - d_io - Wt),
            (0.0, W_mmi / 2 - d_io),
            (-lt, W_mmi / 2 - d_io - Wt / 2 + wt / 2),
        ],

        "out_bot_taper": [
            (L_mmi, -W_mmi / 2 + d_io),
            (L_mmi + lt, -W_mmi / 2 + d_io + Wt / 2 - wt / 2),
            (L_mmi + lt, -W_mmi / 2 + d_io + Wt / 2 + wt / 2),
            (L_mmi, -W_mmi / 2 + d_io + Wt),
        ],

        "out_top_taper": [
            (L_mmi, W_mmi / 2 - d_io - Wt),
            (L_mmi + lt, W_mmi / 2 - d_io - Wt / 2 - wt / 2),
            (L_mmi + lt, W_mmi / 2 - d_io - Wt / 2 + wt / 2),
            (L_mmi, W_mmi / 2 - d_io),
        ],

        "in_bot_wg": [
            (-lt - L_wg, -W_mmi / 2 + d_io + Wt / 2 - wt / 2),
            (-lt,        -W_mmi / 2 + d_io + Wt / 2 - wt / 2),
            (-lt,        -W_mmi / 2 + d_io + Wt / 2 + wt / 2),
            (-lt - L_wg, -W_mmi / 2 + d_io + Wt / 2 + wt / 2),
        ],

        "in_top_wg": [
            (-lt - L_wg, W_mmi / 2 - d_io - Wt / 2 - wt / 2),
            (-lt,        W_mmi / 2 - d_io - Wt / 2 - wt / 2),
            (-lt,        W_mmi / 2 - d_io - Wt / 2 + wt / 2),
            (-lt - L_wg, W_mmi / 2 - d_io - Wt / 2 + wt / 2),
        ],

        "out_bot_wg": [
            (L_mmi + lt,        -W_mmi / 2 + d_io + Wt / 2 - wt / 2),
            (L_mmi + lt + L_wg, -W_mmi / 2 + d_io + Wt / 2 - wt / 2),
            (L_mmi + lt + L_wg, -W_mmi / 2 + d_io + Wt / 2 + wt / 2),
            (L_mmi + lt,        -W_mmi / 2 + d_io + Wt / 2 + wt / 2),
        ],

        "out_top_wg": [
            (L_mmi + lt,        W_mmi / 2 - d_io - Wt / 2 - wt / 2),
            (L_mmi + lt + L_wg, W_mmi / 2 - d_io - Wt / 2 - wt / 2),
            (L_mmi + lt + L_wg, W_mmi / 2 - d_io - Wt / 2 + wt / 2),
            (L_mmi + lt,        W_mmi / 2 - d_io - Wt / 2 + wt / 2),
        ],
    }

    for poly in polys.values():
        c.add_polygon(np.array(poly), layer=layer)

    y_bot = -W_mmi / 2 + d_io + Wt / 2
    y_top = W_mmi / 2 - d_io - Wt / 2
    x_left = -lt - L_wg
    x_right = L_mmi + lt + L_wg

    for name, center, orientation in [
        ("o1", (x_left, y_bot), 180),
        ("o2", (x_left, y_top), 180),
        ("o3", (x_right, y_top), 0),
        ("o4", (x_right, y_bot), 0),
    ]:
        c.add_port(
            name=name,
            center=center,
            width=wt,
            orientation=orientation,
            layer=layer,
        )

    return c

@gf.cell
def mmi_2x2_bends(length_mmi_2x2: float = 262.9723, width: float = TECH.width):
    c = gf.Component()

    mmi_95 = c << b_symmetric_mmi(length_mmi_2x2)
    b1 = c << bend_s(size = [50, 15], cross_section = "strip", width = width, allow_min_radius_violation = True)
    b2 = c << bend_s(size = [50, 15], cross_section = "strip", width = width, allow_min_radius_violation = True)
    b1.mirror_y()
    b1.dmovex(mmi_95.ports['o4'].dx).dmovey(mmi_95.ports['o4'].dy)
    b2.dmovex(mmi_95.ports["o3"].dx).dmovey(mmi_95.ports["o3"].dy)

    b3 = c << bend_s(size = [50, 15], cross_section = "strip", width = width, allow_min_radius_violation = True)
    b4 = c << bend_s(size = [50, 15], cross_section = "strip", width = width, allow_min_radius_violation = True)
    b3.mirror_x()
    b3.mirror_y()
    b3.dmovex(mmi_95.ports["o1"].dx).dmovey(mmi_95.ports["o1"].dy)
    b4.mirror_x()
    b4.dmovex(mmi_95.ports["o2"].dx).dmovey(mmi_95.ports["o2"].dy)

    c.add_port(name = "o2", port = b4.ports["o2"], port_type = "optical")
    c.add_port(name = "o1", port = b3.ports["o2"], port_type = "optical")
    c.add_port(name = "o3", port = b2.ports["o2"], port_type = "optical")
    c.add_port(name = "o4", port = b1.ports["o2"], port_type = "optical")

    #normalizar posición para que quede en (0,0)
    x0, y0 = c.ports["o1"].dcenter
    c.dmove((-x0, -y0))

    return c


@gf.cell
def mmi3x3(
    width: float = TECH.width,
    width_taper: float = 1.0,
    length_taper: float = 10.0,
    length_mmi: float = 20.0,
    width_mmi: float = 6.0,
    gap_mmi: float = 0.25,
    taper: ComponentSpec = gf.components.taper,
    straight: ComponentSpec = gf.components.straight,
    cross_section: CrossSectionSpec = "strip",
) -> Component:
    c = gf.Component()

    gap_mmi = gf.snap.snap_to_grid(gap_mmi, grid_factor=2) #ajusta el gap a la rejilla para evitar decimales raros que queden fuera del grid

    x = gf.get_cross_section(cross_section)
    width = width or x.width
    w_taper = width_taper

    _taper = gf.get_component(
        taper,
        length=length_taper,
        width1=width,
        width2=w_taper,
        cross_section=cross_section,
    )

    pitch = w_taper + gap_mmi

    y_bot = -pitch
    y_mid = 0
    y_top = +pitch

    _ = c << gf.get_component(
        straight,
        length=length_mmi,
        width=width_mmi,
        cross_section=cross_section,
    )

    temp_component = Component() #para definir los puertos ideales (temporales)

    ports = [
        temp_component.add_port(
            name="o1",
            orientation=180,
            center=(0, y_bot),
            width=w_taper,
            cross_section=x,
        ),
        temp_component.add_port(
            name="o2",
            orientation=180,
            center=(0, y_mid),
            width=w_taper,
            cross_section=x,
        ),
        temp_component.add_port(
            name="o3",
            orientation=180,
            center=(0, y_top),
            width=w_taper,
            cross_section=x,
        ),
        temp_component.add_port(
            name="o4",
            orientation=0,
            center=(length_mmi, y_top),
            width=w_taper,
            cross_section=x,
        ),
        temp_component.add_port(
            name="o5",
            orientation=0,
            center=(length_mmi, y_mid),
            width=w_taper,
            cross_section=x,
        ),
        temp_component.add_port(
            name="o6",
            orientation=0,
            center=(length_mmi, y_bot),
            width=w_taper,
            cross_section=x,
        ),
    ]

    for port in ports:
        taper_ref = c << _taper
        taper_ref.connect(
            port="o2",
            other=port,
            allow_width_mismatch=True,
        )
        c.add_port(name=port.name, port=taper_ref.ports["o1"])

    c.flatten()
    return c

@gf.cell
def spiral_upv(
    radius: float = TECH.radius,
    N_spr: int = 5,
    d_SPR: float = 7.0,
    dx_SPR: float = 10.0,
    dy_SPR: float = 10.0,
    layer: CrossSectionSpec = "strip",
    ) -> gf.Component:
   
    """Returns a spiral.
 
    Pending: add ports, check whether it works as other (native) spirals
    Use partial with this?
 
    Args:
        radius: spiral radius.
        N_spr: order-number of loops (0,1,...)
        d_SPR: waveguide separation
        dx_SPR: spiral straight extent in x
        dy_SPR: spiral straight extent in y
        layer: extruding in a specified layer (or cross section)
    """
 
    # Path definitions
    P = gf.Path()
    P1 = gf.Path()
    P2 = gf.Path()
 
    # Involed lengths
    lx0 = gf.path.straight(dx_SPR + d_SPR + 2*radius)
    ldy = gf.path.straight(dy_SPR)
    ld = gf.path.straight(d_SPR)
    ly0 = ldy+ld
 
    # 90 degree curves
    parcL = gf.path.arc(radius=radius, angle=90)
    parcR = gf.path.arc(radius=radius, angle=-90)
 
    # Zero-th order
    P01 = ld+ld + ly0 + parcL + lx0 + parcL + ly0 + parcL + gf.path.straight(dx_SPR/2)
    P02 = gf.path.straight(dx_SPR/2) + parcR + ly0
    P0 =  P01 + parcL + ldy + parcR + P02
 
    P = P0
    lx = lx0
    ly = ly0 + ld + ld
 
    # Generating loops
    for i in range(1,N_spr+1):
   
        if i == N_spr:
            if i % 2 == 1:
             P1 = parcR + (lx) + parcR + (ly) + parcR + (lx+ld+ld) + parcR + (ly+ld)
             P = P + P1
            else:
             P1 = (ly+ld) + parcL + (lx+ld+ld) + parcL + (ly) + parcL + (lx) + parcL
             P = P1 + P
        else:  
            if i % 2 == 1:
             P1 = parcR + (lx) + parcR + (ly) + parcR + (lx+ld+ld) + parcR + (ly+ld+ld)
             P = P + P1
            else:
             P1 = (ly+ld+ld) + parcL + (lx+ld+ld) + parcL + (ly) + parcL + (lx) + parcL
             P = P1 + P
       
        lx = lx + ld + ld
        ly = ly + ld + ld
 
   
    # End feet
    if N_spr % 2 == 1: P =  (lx + parcL) + P + parcL
    else: P =  parcR + P + (parcR + lx)
 
    # f = P.plot()
 
    # if N_spr % 2 == 0:
        # P = P.rotate(90)
        # P = P.()
        # P = P.(
        # p1=(0, 1), p2=(0, 0))
 
    # Extrude
    PDK = gf.get_active_pdk()
    PDK.activate()
    c = gf.path.extrude(P, cross_section=layer)

    x0, y0 = c.ports["o1"].dcenter
    c.dmove((-x0, -y0))
 
    spr_length = P.length()
    c.info["length"] = float(gf.snap.snap_to_grid(spr_length))
    c.info["lx_final"] = float(lx.length())
 
    return c

from scipy.optimize import minimize
import numpy as np
 

def define_spiral_length(delay_length=10000,
                         N_spr=7,
                         radius=125,
                         d_SPR=10,
                         dy_SPR=20,
                         ):
    """Defines the spiral straight length based on the desired delay_length"""
    print("Defining spiral length for delay:", delay_length)
    def f(x):
        spiral_to_test = partial(spiral_upv, N_spr=N_spr ,dx_SPR=x[0], radius=radius, d_SPR=d_SPR, dy_SPR=dy_SPR)
        device = spiral_to_test()
        current_delay_length = device.info["length"]
        #print("Current spiral length:", current_delay_length, "for dx_SPR:", x[0])
        cost = current_delay_length - delay_length
        return np.abs(cost)
    length_spiral = minimize(f, x0=np.array(200.0), method='Nelder-Mead',tol=1e-2, bounds=((10, 5000.0),)).x[0]
    print("Spiral length set to:", length_spiral)
    return length_spiral

@gf.cell
def bend_euler(
    radius: float = TECH.radius_strip,
    angle: float = 90,
    p: float = 0.5,
    width: float = TECH.width,
    cross_section: CrossSectionSpec = "strip",
    allow_min_radius_violation: bool = False,
) -> gf.Component:
    """Regular degree euler bend.

    Args:
        radius: in um. Defaults to cross_section_radius.
        angle: total angle of the curve.
        p: Proportion of the curve that is an Euler curve.
        width: width to use. Defaults to cross_section.width.
        cross_section: specification (CrossSection, string, CrossSectionFactory dict).
        allow_min_radius_violation: if True allows radius to be smaller than cross_section radius.
    """
    return gf.c.bend_euler(
        radius=radius,
        angle=angle,
        p=p,
        width=width,
        cross_section=cross_section,
        allow_min_radius_violation=allow_min_radius_violation,
        with_arc_floorplan=True,
        npoints=None,
        layer=None,
    )

@gf.cell
def bend_s(
    size: Size = (50, 10),
    cross_section: CrossSectionSpec = "strip",
    width: float | None = None,
    allow_min_radius_violation: bool = False,
) -> gf.Component:
    """Return S bend with bezier curve.

    stores min_bend_radius property in self.info['min_bend_radius']
    min_bend_radius depends on height and length

    Args:
        size: in x and y direction.
        cross_section: spec.
        width: width of the waveguide. If None, it will use the width of the cross_section.
        allow_min_radius_violation: allows min radius violations.
    """
    return gf.c.bend_s(
        size=size,
        cross_section=cross_section,
        npoints=99,
        allow_min_radius_violation=allow_min_radius_violation,
        width=width,
    )

def terminator(number_of_loops: float=6, min_bend_radius = 125, width_tip = 0.6, separation = 1.5): 
    return gf.components.terminator_spiral(number_of_loops=number_of_loops, min_bend_radius=min_bend_radius, width_tip=width_tip, separation = 1.5)
 


##################################################################################################################################

#                                                   CIRCUITO

##################################################################################################################################

@gf.cell
def wvl_tracker(length_spiral: float = 2120.00732421875, L = 3000,  length_mmi_2x2: float =126.3,  taper_length = 50 + 20,   length_mmi_3x3: float =  242.4723, taper_width_mmi_3x3: float = 2.8, gap_mmi_3x3: float = 0.2,  width: float = TECH.width, radius: float =  TECH.radius): #mejorarlo poniendo las funciones de espiral dentro
    c = gf.Component()
   
    mmi_95 = c << mmi_2x2_bends(length_mmi_2x2)
    mmi_33 = c << mmi3x3(width, width_taper=taper_width_mmi_3x3, length_taper= taper_length, length_mmi = length_mmi_3x3, width_mmi= 10, gap_mmi = gap_mmi_3x3)
    spiral = c << spiral_upv(radius = radius, N_spr = 18 , d_SPR =10 , dx_SPR= length_spiral, dy_SPR = 50.46, layer = "strip") # N must BE EVEN 

    
    
    h = spiral.ports["o2"].dx - spiral.ports["o1"].dx
    wvg_up = c << gf.components.straight(length = L, cross_section= "strip", width = width)

    dy_mmi95 = mmi_95.ports["o3"].dy - mmi_95.ports["o4"].dy #para conectar los s_bend de forma que las entradas a los mmi queden a la misma altura
    dy_mmi33 = mmi_33.ports["o3"].dy - mmi_33.ports["o1"].dy
    h_bends_33 = ( dy_mmi95 - dy_mmi33)/2
    b3 = c << bend_s(size = [50, h_bends_33], cross_section = "strip", width = width, allow_min_radius_violation = True)
    b4 = c << bend_s(size = [50, h_bends_33], cross_section = "strip", width = width, allow_min_radius_violation = True)

    wvg_up.dmove((mmi_95.ports['o3'].dx, mmi_95.ports['o3'].dy))
    b3.dmirror_y()
    b3.dmove((wvg_up.ports['o2'].dx, wvg_up.ports['o2'].dy))
    mmi_33.dmove((b3.ports['o2'].dx + taper_length, b3.ports['o2'].dy - 3)) # 3 = Wt
    b4.dmirror_x()
    b4.dmirror_y()
    b4.dmove((mmi_33.ports['o2'].dx, mmi_33.ports['o1'].dy))
    
    dx_spiral = np.abs(mmi_95.ports['o4'].dx - spiral.ports['o1'].dx)
    dy_spiral = np.abs(mmi_95.ports['o4'].dy - spiral.ports['o1'].dy)

    spiral.dmove((dx_spiral, -dy_spiral))

    

      #bends entrada y salida cto
    b7 = c << bend_s(size = [50, h_bends_33], cross_section = "strip", width = width, allow_min_radius_violation = True)
    b8 = c << bend_s(size = [50, h_bends_33], cross_section = "strip", width = width, allow_min_radius_violation = True)
    wvg = c << gf.components.straight(10, cross_section = "strip")
    b7.mirror_y()
    b8.dmovex(mmi_33.ports["o4"].dx).dmovey(mmi_33.ports["o4"].dy)
    b7.dmovex(mmi_33.ports["o6"].dx).dmovey(mmi_33.ports["o6"].dy)
    wvg.dmovex(mmi_33.ports["o5"].dx).dmovey(mmi_33.ports["o5"].dy)



    c.add_port(name = "o1", port = mmi_95.ports["o1"], port_type= "optical")
    c.add_port(name = "o2", port = mmi_95.ports["o2"], port_type= "optical")
    c.add_port(name = "o3", port = b8.ports["o2"], port_type= "optical")
    c.add_port(name = "o4", port = wvg.ports["o2"], port_type= "optical")
    c.add_port(name = "o5", port = b7.ports["o2"], port_type= "optical")


    c.info["total_length_device"] = 2*taper_length + length_mmi_2x2 + 2*10 + h  + 2*taper_length + length_mmi_3x3 #2*10 es de los sbends
    c.info["length_short_arm"] = h + 2*10
    c.info["h_bends_33"] = h_bends_33

    #normalizar posición para que quede en (0,0)
    
    x0, y0 = c.ports["o1"].dcenter
    c.dmove((-x0, -y0))

    return c 


def wvl_tracker_with_term(length_spiral: float = 2120.00732421875, L = 3000,  length_mmi_2x2: float =126.3,  taper_length = 50 + 20,   length_mmi_3x3: float =  242.4723, taper_width_mmi_3x3: float = 2.8, gap_mmi_3x3: float = 0.2,  width: float = TECH.width, radius: float =  TECH.radius): #mejorarlo poniendo las funciones de espiral dentro
    c = gf.Component()
   
    mmi_95 = c << mmi_2x2_bends(length_mmi_2x2)
    mmi_33 = c << mmi3x3(width, width_taper=taper_width_mmi_3x3, length_taper= taper_length, length_mmi = length_mmi_3x3, width_mmi= 10, gap_mmi = gap_mmi_3x3)
    spiral = c << spiral_upv(radius = radius, N_spr = 18 , d_SPR =10 , dx_SPR= length_spiral, dy_SPR = 50.46, layer = "strip") # N must BE EVEN 

    
    
    h = spiral.ports["o2"].dx - spiral.ports["o1"].dx
    wvg_up = c << gf.components.straight(length = L, cross_section= "strip", width = width)

    dy_mmi95 = mmi_95.ports["o3"].dy - mmi_95.ports["o4"].dy #para conectar los s_bend de forma que las entradas a los mmi queden a la misma altura
    dy_mmi33 = mmi_33.ports["o3"].dy - mmi_33.ports["o1"].dy
    h_bends_33 = ( dy_mmi95 - dy_mmi33)/2
    b3 = c << bend_s(size = [50, h_bends_33], cross_section = "strip", width = width, allow_min_radius_violation = True)
    b4 = c << bend_s(size = [50, h_bends_33], cross_section = "strip", width = width, allow_min_radius_violation = True)

    wvg_up.dmove((mmi_95.ports['o3'].dx, mmi_95.ports['o3'].dy))
    b3.dmirror_y()
    b3.dmove((wvg_up.ports['o2'].dx, wvg_up.ports['o2'].dy))
    mmi_33.dmove((b3.ports['o2'].dx + taper_length, b3.ports['o2'].dy - 3)) # 3 = Wt
    b4.dmirror_x()
    b4.dmirror_y()
    b4.dmove((mmi_33.ports['o2'].dx, mmi_33.ports['o1'].dy))
    
    dx_spiral = np.abs(mmi_95.ports['o4'].dx - spiral.ports['o1'].dx)
    dy_spiral = np.abs(mmi_95.ports['o4'].dy - spiral.ports['o1'].dy)

    spiral.dmove((dx_spiral, -dy_spiral))

    

      #bends entrada y salida cto
    b7 = c << bend_s(size = [50, h_bends_33], cross_section = "strip", width = width, allow_min_radius_violation = True)
    b8 = c << bend_s(size = [50, h_bends_33], cross_section = "strip", width = width, allow_min_radius_violation = True)
    wvg = c << gf.components.straight(10, cross_section = "strip")
    b7.mirror_y()
    b8.dmovex(mmi_33.ports["o4"].dx).dmovey(mmi_33.ports["o4"].dy)
    b7.dmovex(mmi_33.ports["o6"].dx).dmovey(mmi_33.ports["o6"].dy)
    wvg.dmovex(mmi_33.ports["o5"].dx).dmovey(mmi_33.ports["o5"].dy)

    wvg_term = c <<  gf.components.straight(length = 10, cross_section= "strip", width = width)
    wvg_term.dmove((mmi_33.ports['o2'].dx - 10, mmi_33.ports['o2'].dy ))

    b9 = c << bend_s(size = [50, 10], cross_section = "strip", width = width, allow_min_radius_violation = True)
    b9.mirror_x()
    b9.dmove((wvg_term.ports['o1'].dx, wvg_term.ports['o1'].dy ))
    wvg_term_2 = c <<  gf.components.straight(length = 10, cross_section= "strip", width = width)
    wvg_term_2.dmove((b9.ports['o2'].dx - 10, b9.ports['o2'].dy ))
    term = c << terminator(number_of_loops= 1,min_bend_radius=10, separation = 0.3)
    term.connect(port = 'o1', other = wvg_term_2.ports['o1'])
   


    c.add_port(name = "o1", port = mmi_95.ports["o1"], port_type= "optical")
    c.add_port(name = "o2", port = mmi_95.ports["o2"], port_type= "optical")
    c.add_port(name = "o3", port = b8.ports["o2"], port_type= "optical")
    c.add_port(name = "o4", port = wvg.ports["o2"], port_type= "optical")
    c.add_port(name = "o5", port = b7.ports["o2"], port_type= "optical")


    c.info["total_length_device"] = 2*taper_length + length_mmi_2x2 + 2*10 + h  + 2*taper_length + length_mmi_3x3 #2*10 es de los sbends
    c.info["length_short_arm"] = h + 2*10
    c.info["h_bends_33"] = h_bends_33

    #normalizar posición para que quede en (0,0)
    
    x0, y0 = c.ports["o1"].dcenter
    c.dmove((-x0, -y0))

    return c 

################################################################################################################################################

#                                                    ESTRUCTURAS TEST

################################################################################################################################################

@gf.cell
def mmi_3x3_test(length_mmi_3x3: float =  242.4723, taper_width_mmi_3x3: float = 2.8, gap_mmi_3x3: float = 0.2, taper_length: float = 10, width: float = TECH.width): #altura bends heredado de cto: h_bends_33

    c = gf.Component()
    wvl_tracker = wvl_tracker_with_term()
    altura_bends = wvl_tracker.info['h_bends_33']

    mmi_33 = c << mmi3x3(width= width, width_taper=taper_width_mmi_3x3, length_taper= taper_length, length_mmi = length_mmi_3x3, width_mmi= 10, gap_mmi = gap_mmi_3x3)
    b1 = c << bend_s(size = [50, altura_bends], cross_section = "strip", width = width, allow_min_radius_violation = True)
    b2 = c << bend_s(size = [50, altura_bends], cross_section = "strip", width = width, allow_min_radius_violation = True)
    b3 = c << bend_s(size = [50, altura_bends], cross_section = "strip", width = width, allow_min_radius_violation = True)
    b4 = c << bend_s(size = [50, altura_bends], cross_section = "strip", width = width, allow_min_radius_violation = True)
    wvg = c << gf.components.straight(50, cross_section = "strip")
    
    b1.mirror_x()
    b1.mirror_y()
    b1.dmovex(mmi_33.ports["o1"].dx).dmovey(mmi_33.ports["o1"].dy)
    b2.mirror_x()
    b2.dmovex(mmi_33.ports["o3"].dx).dmovey(mmi_33.ports["o3"].dy)
    b3.mirror_y()
    b4.dmovex(mmi_33.ports["o4"].dx).dmovey(mmi_33.ports["o4"].dy)
    b3.dmovex(mmi_33.ports["o6"].dx).dmovey(mmi_33.ports["o6"].dy)
    wvg.dmovex(mmi_33.ports["o5"].dx).dmovey(mmi_33.ports["o5"].dy)
    
    wvg_term = c <<  gf.components.straight(length = 10, cross_section= "strip", width = width)
    wvg_term.dmove((mmi_33.ports['o2'].dx - 10, mmi_33.ports['o2'].dy ))
    b9 = c << bend_s(size = [50, 10], cross_section = "strip", width = width, allow_min_radius_violation = True)
    b9.mirror_x()
    b9.dmove((wvg_term.ports['o1'].dx, wvg_term.ports['o1'].dy ))
    wvg_term_2 = c <<  gf.components.straight(length = 10, cross_section= "strip", width = width)
    wvg_term_2.dmove((b9.ports['o2'].dx - 10, b9.ports['o2'].dy ))
    term = c << terminator(number_of_loops= 1,min_bend_radius=10, separation = 0.3)
    term.connect(port = 'o1', other = wvg_term_2.ports['o1'])
   

    c.add_port(name = "o2", port = b2.ports["o2"], port_type = "optical")
    c.add_port(name = "o1", port = b1.ports["o2"], port_type = "optical")
    c.add_port(name = "o3", port = b4.ports["o2"], port_type = "optical")
    c.add_port(name = "o4", port = wvg.ports["o2"], port_type = "optical")
    c.add_port(name = "o5", port = b3.ports["o2"], port_type = "optical")
    
    #normalizar posición para que quede en (0,0)
    x0, y0 = c.ports["o1"].dcenter
    c.dmove((-x0, -y0))

    return c


@gf.cell
def mmi_ts(
    mmi: ComponentSpec = "mmi2x2",
    x_total: float = 10000,
    x_margin: float = 250,
    y_total: float = 3*127,
    invert: bool = False,
    n: int = 4,
    add_terminators: bool = False,  
) -> gf.Component:
    c = gf.Component()
    mmi = gf.get_component(mmi)
    mmi_xsize = mmi['o3'].dx - mmi['o1'].dx
    mmi_ysize = mmi['o2'].dy - mmi['o1'].dy
    # print(mmi_xsize)
    # print(mmi_ysize)
 
    if n == 1:
        x_pad = 0
        y_pad = 0
    else:
        x_pad = (1/(n-1))*(x_total - 2*x_margin - n*mmi_xsize)
        y_pad = (1/(n-1))*y_total - mmi_ysize
 
    # print(x_pad)
    # print(y_pad)
 
    mmis = []
    for i in np.arange(0,n):
        mmis.append(c.add_ref(mmi))
        mmis[i].dmovex(i*(x_pad+mmi_xsize)).dmovey((-1)**(int(invert))*i*(y_pad+mmi_ysize))
 
    c.add_port(name = f'o1', port = mmis[0].ports['o1'])
    c.add_port(name = f'o2', port = mmis[0].ports['o2'])
    port_count = 2
 
    # invert=False  -> variante "bar"  : conecta o3 -> o2 del siguiente, tap = o4
    # invert=True   -> variante "cross": conecta o4 -> o2 del siguiente, tap = o3
    cascade_out_port = "o4" if invert else "o3"
    tap_port = "o3" if invert else "o4"
    next_input_port = "o2"
    unused_input_port = "o1"
 
    for i, mmi_ref in enumerate(mmis):
        if (i != (n-1)):
            gf.routing.route_single_sbend(
                c,
                mmi_ref[cascade_out_port],            
                mmis[i+1][next_input_port],          
                cross_section='strip'
            )
 
            if add_terminators:
                term = c.add_ref(gf.components.terminator_spiral(number_of_loops=6,
                                                                 min_bend_radius=35,
                                                                 width_tip=0.6))
                term.connect("o1", mmis[i+1].ports[unused_input_port])
 
            c.add_port(name = f'o{port_count+1}', port = mmi_ref.ports[tap_port])
            port_count += 1
 
    c.add_port(name = f'o{port_count+1}', port = mmis[n-1].ports[cascade_out_port])
    port_count += 1
    c.add_port(name = f'o{port_count+1}', port = mmis[n-1].ports[tap_port])
 
    return c

@gf.cell
def die_with_gratings(
    size: tuple[float, float] = (10000, 5000),
    ngratings: int = 34,
    grating_pitch: float = 125.0,
    grating_coupler: ComponentSpec | None = "grating_coupler_rectangular",
    cross_section: CrossSectionSpec = "strip",
    layer_floorplan: LayerSpec = "FLOORPLAN",
    edge_to_grating_distance: float = 150.0,
    with_loopback: bool = False,
    border: float = 125,
) -> gf.Component:
    """A die with grating couplers.

    Args:
        size: the size of the die, in um.
        ngratings: the number of grating couplers.
        grating_pitch: the pitch of the grating couplers, in um.
        grating_coupler: the grating coupler component. None skips the grating couplers.
        cross_section: the cross section.
        layer_floorplan: the layer of the floorplan.
        edge_to_grating_distance: the distance from the edge to the grating couplers, in um.
        with_loopback: if True, adds a loopback between edge GCs. Only works for rotation = 90 for now.
        border: the border size, in um.
    """
    c = gf.Component()
    ob = gf.components.rectangle(
        size=size, layer=layer_floorplan, centered=True, port_type=None
    )
    ib = gf.components.rectangle(
        size=(size[0]-border*2,size[1]-border*2), centered=True, layer=layer_floorplan
    )
    #ib.dmovex(border).dmovey(border)
    fp = c << gf.boolean(A=ob, B=ib, operation="A-B", layer=layer_floorplan)
    xs, ys = size
    x0 = xs / 2 + edge_to_grating_distance
    if grating_coupler:
        gca = gf.c.grating_coupler_array(
            n=ngratings,
            pitch=grating_pitch,
            with_loopback=with_loopback,
            grating_coupler=grating_coupler,
            cross_section=cross_section,
        )
        left = c << gca
        left.rotate(-90)
        left.xmin = -xs / 2 + edge_to_grating_distance
        left.y = fp.y
        c.add_ports(left.ports, prefix="W")
        right = c << gca
        right.rotate(+90)
        right.xmax = xs / 2 - edge_to_grating_distance
        right.y = fp.y
        c.add_ports(right.ports, prefix="E")

    c.auto_rename_ports()
    c.dmovex(0.5*size[0]).dmovey(0.5*size[1])
    for i, port in enumerate(c.ports):
        text = c.add_ref(gf.components.text(
            text=f"P{i}", size=25, layer=LAYER.WG))
        text.dmovex(port.dx+20).dmovey(port.dy+20)
        text = c.add_ref(gf.components.text(
            text=f"P{i}", size=25, layer=LAYER.HEATER))
        text.dmovex(port.dx+20).dmovey(port.dy+20)
        #print(port)
    return c
