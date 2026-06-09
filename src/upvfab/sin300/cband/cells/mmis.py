"""This module contains the building blocks for the UPVfab PDK."""

from functools import partial

import gdsfactory as gf
from gdsfactory.typings import (
    CrossSectionSpec,
)
from upvfab.sin300.cband.tech import LAYER, TECH
from upvfab.sin300.cband.tech import cross_sections as xs



############################
# MMI PARAMETERS
############################
# This section defines all MMI dimensions used throughout the module.
# Modify these values to tune MMI devices for your technology.
# Three variants are defined: _C (C-Band), _L (L-Band), _S (S-Band) for different MMI designs


################
# MMI 2x2 Variants
################

class Params_MMI2x2_C:
    """MMI2x2 parameters (C-Band) for CNM-UPVfab SiN PDK."""
    
    # ===== Strip Waveguides =====
    width_taper: float = 3.1  # Taper width at MMI body base (um)
    length_taper: float = 30.0  # Taper length (um)
    length: float = 105.0  # MMI body length (um) - compact design
    width: float = 12.2  # MMI body width (um)
    gap: float = 0.9  # Gap between tapers at MMI body (um)
    
    # ===== Rib Waveguides =====
    length_rib: float = 105.0  # MMI body length for rib (um)
    gap_rib: float = 1.1  # Gap between tapers at MMI body for rib (um)
    
    # ===== Default Waveguide Width =====
    default_width: float = 1.0  # Default waveguide width (um)


class Params_MMI2x2_L:
    """MMI2x2 parameters (L-Band) for CNM-UPVfab SiN PDK."""
    
    # ===== Strip Waveguides =====
    width_taper: float = 3.1  # Taper width at MMI body base (um)
    length_taper: float = 30.0  # Taper length (um)
    length: float = 95.5  # MMI body length (um) - standard length
    width: float = 12.2  # MMI body width (um)
    gap: float = 0.9  # Gap between tapers at MMI body (um)
    
    # ===== Rib Waveguides =====
    length_rib: float = 95.5  # MMI body length for rib (um)
    gap_rib: float = 1.1  # Gap between tapers at MMI body for rib (um)
    
    # ===== Default Waveguide Width =====
    default_width: float = 1.0  # Default waveguide width (um)


class Params_MMI2x2_S:
    """MMI2x2 parameters (S-Band) for CNM_UPVfab SiN PDK."""
    
    # ===== Strip Waveguides =====
    width_taper: float = 3.1  # Taper width at MMI body base (um)
    length_taper: float = 30.0  # Taper length (um)
    length: float = 114.5  # MMI body length (um) - extended design
    width: float = 12.2  # MMI body width (um)
    gap: float = 0.9  # Gap between tapers at MMI body (um)
    
    # ===== Rib Waveguides =====
    length_rib: float = 114.5  # MMI body length for rib (um)
    gap_rib: float = 1.1  # Gap between tapers at MMI body for rib (um)
    
    # ===== Default Waveguide Width =====
    default_width: float = 1.0  # Default waveguide width (um)


################
# MMI 2x2 85/15 Variants
################

class Params_MMI2x2_85_15_C:
    """MMI2x2 85/15 parameters (C-Band) for CNM-UPVfab SiN PDK."""
    
    # ===== Strip Waveguides =====
    width_taper: float = 3.6  # Taper width at MMI body base (um)
    length_taper: float = 30.0  # Taper length (um)
    length: float = 155  # MMI body length (um) - optimized for 85/15 split
    width: float = 12.2  # MMI body width (um)
    gap: float = 2.4  # Gap between tapers at MMI body (um)
    
    # ===== Rib Waveguides =====
    length_rib: float = 155  # MMI body length for rib (um)
    gap_rib: float = 3.1  # Gap between tapers at MMI body for rib (um)
    
    # ===== Default Waveguide Width =====
    default_width: float = 1.0  # Default waveguide width (um)


class Params_MMI2x2_85_15_L:
    """MMI2x2 85/15 parameters (L-Band) for CNM-UPVfab SiN PDK."""
    
    # ===== Strip Waveguides =====
    width_taper: float = 3.6  # Taper width at MMI body base (um)
    length_taper: float = 30.0  # Taper length (um)
    length: float = 143  # MMI body length (um) - optimized for 85/15 split
    width: float = 12.2  # MMI body width (um)
    gap: float = 2.4  # Gap between tapers at MMI body (um)
    
    # ===== Rib Waveguides =====
    length_rib: float = 143  # MMI body length for rib (um)
    gap_rib: float = 3.1  # Gap between tapers at MMI body for rib (um)
    
    # ===== Default Waveguide Width =====
    default_width: float = 1.0  # Default waveguide width (um)


class Params_MMI2x2_85_15_S:
    """MMI2x2 85/15 parameters (S-Band) for CNM_UPVfab SiN PDK."""
    
    # ===== Strip Waveguides =====
    width_taper: float = 3.6  # Taper width at MMI body base (um)
    length_taper: float = 30.0  # Taper length (um)
    length: float = 167  # MMI body length (um) - optimized for 85/15 split
    width: float = 12.2  # MMI body width (um)
    gap: float = 2.4  # Gap between tapers at MMI body (um)
    
    # ===== Rib Waveguides =====
    length_rib: float = 167  # MMI body length for rib (um)
    gap_rib: float = 3.1  # Gap between tapers at MMI body for rib (um)
    
    # ===== Default Waveguide Width =====
    default_width: float = 1.0  # Default waveguide width (um)


################
# MMIs 2x2
################

def _mmi2x2_with_sbends(
    width: float,
    width_taper: float,
    length_taper: float,
    length_mmi: float,
    width_mmi: float,
    gap_mmi: float,
    cross_section: CrossSectionSpec,
) -> gf.Component:
    from upvfab.sin300.cband import PDK

    mmi_c = gf.c.mmi2x2(
        width=width,
        width_taper=width_taper,
        length_taper=length_taper,
        length_mmi=length_mmi,
        width_mmi=width_mmi,
        gap_mmi=gap_mmi,
        cross_section=cross_section,
    )
    s_u = PDK.cells["bend_s"](size=(50, 10))
    s_d = PDK.cells["bend_s"](size=(-50, 10))

    c = gf.Component("mmi2x2")
    mmi_ref = c.add_ref(mmi_c)
    s1 = c.add_ref(s_u)
    s2 = c.add_ref(s_d)
    s3 = c.add_ref(s_u)
    s4 = c.add_ref(s_d)
    s3.connect("o1", mmi_ref.ports["o3"])
    s4.connect("o1", mmi_ref.ports["o4"])
    s1.connect("o2", mmi_ref.ports["o1"])
    s2.connect("o2", mmi_ref.ports["o2"])
    c.add_port(name="o1", port=s1.ports["o1"])
    c.add_port(name="o2", port=s2.ports["o1"])
    c.add_port(name="o3", port=s3.ports["o2"])
    c.add_port(name="o4", port=s4.ports["o2"])
    return c

@gf.cell
def mmi2x2_c(
    width: float = Params_MMI2x2_C.default_width,
    width_taper: float = Params_MMI2x2_C.width_taper,
    length_taper: float = Params_MMI2x2_C.length_taper,
    length_mmi: float = Params_MMI2x2_C.length,
    width_mmi: float = Params_MMI2x2_C.width,
    gap_mmi: float = Params_MMI2x2_C.gap,
    cross_section: CrossSectionSpec = xs['strip'],
) -> gf.Component:
    """An mmi2x2 (C-Band).

    An mmi2x2 is a 2x2 splitter

    Args:
        width: the width of the waveguides connecting at the mmi ports
        width_taper: the width at the base of the mmi body
        length_taper: the length of the tapers going towards the mmi body
        length_mmi: the length of the mmi body
        width_mmi: the width of the mmi body
        gap_mmi: the gap between the tapers at the mmi body
        cross_section: a cross section or its name or a function generating a cross section.
    """
    return _mmi2x2_with_sbends(
        width=width,
        width_taper=width_taper,
        length_taper=length_taper,
        length_mmi=length_mmi,
        width_mmi=width_mmi,
        gap_mmi=gap_mmi,
        cross_section=cross_section,
    )


@gf.cell
def mmi2x2_l(
    width: float = Params_MMI2x2_L.default_width,
    width_taper: float = Params_MMI2x2_L.width_taper,
    length_taper: float = Params_MMI2x2_L.length_taper,
    length_mmi: float = Params_MMI2x2_L.length,
    width_mmi: float = Params_MMI2x2_L.width,
    gap_mmi: float = Params_MMI2x2_L.gap,
    cross_section: CrossSectionSpec = xs['strip'],
) -> gf.Component:
    """An mmi2x2 (L-Band).

    An mmi2x2 is a 2x2 splitter

    Args:
        width: the width of the waveguides connecting at the mmi ports
        width_taper: the width at the base of the mmi body
        length_taper: the length of the tapers going towards the mmi body
        length_mmi: the length of the mmi body
        width_mmi: the width of the mmi body
        gap_mmi: the gap between the tapers at the mmi body
        cross_section: a cross section or its name or a function generating a cross section.
    """
    return _mmi2x2_with_sbends(
        width=width,
        width_taper=width_taper,
        length_taper=length_taper,
        length_mmi=length_mmi,
        width_mmi=width_mmi,
        gap_mmi=gap_mmi,
        cross_section=cross_section,
    )


@gf.cell
def mmi2x2_s(
    width: float = Params_MMI2x2_S.default_width,
    width_taper: float = Params_MMI2x2_S.width_taper,
    length_taper: float = Params_MMI2x2_S.length_taper,
    length_mmi: float = Params_MMI2x2_S.length,
    width_mmi: float = Params_MMI2x2_S.width,
    gap_mmi: float = Params_MMI2x2_S.gap,
    cross_section: CrossSectionSpec = xs['strip'],
) -> gf.Component:
    """An mmi2x2 (S-Band).

    An mmi2x2 is a 2x2 splitter

    Args:
        width: the width of the waveguides connecting at the mmi ports
        width_taper: the width at the base of the mmi body
        length_taper: the length of the tapers going towards the mmi body
        length_mmi: the length of the mmi body
        width_mmi: the width of the mmi body
        gap_mmi: the gap between the tapers at the mmi body
        cross_section: a cross section or its name or a function generating a cross section.
    """
    return _mmi2x2_with_sbends(
        width=width,
        width_taper=width_taper,
        length_taper=length_taper,
        length_mmi=length_mmi,
        width_mmi=width_mmi,
        gap_mmi=gap_mmi,
        cross_section=cross_section,
    )


################
# MMIs 2x2 85/15
################

@gf.cell
def mmi2x2_85_15_c(
    width: float = Params_MMI2x2_85_15_C.default_width,
    width_taper: float = Params_MMI2x2_85_15_C.width_taper,
    length_taper: float = Params_MMI2x2_85_15_C.length_taper,
    length_mmi: float = Params_MMI2x2_85_15_C.length,
    width_mmi: float = Params_MMI2x2_85_15_C.width,
    gap_mmi: float = Params_MMI2x2_85_15_C.gap,
    cross_section: CrossSectionSpec = xs['strip'],
) -> gf.Component:
    """An mmi2x2 85/15 (C-Band).

    An asymmetric 2x2 splitter with 85/15 power split ratio

    Args:
        width: the width of the waveguides connecting at the mmi ports
        width_taper: the width at the base of the mmi body
        length_taper: the length of the tapers going towards the mmi body
        length_mmi: the length of the mmi body
        width_mmi: the width of the mmi body
        gap_mmi: the gap between the tapers at the mmi body
        cross_section: a cross section or its name or a function generating a cross section.
    """
    return _mmi2x2_with_sbends(
        width=width,
        width_taper=width_taper,
        length_taper=length_taper,
        length_mmi=length_mmi,
        width_mmi=width_mmi,
        gap_mmi=gap_mmi,
        cross_section=cross_section,
    )


@gf.cell
def mmi2x2_85_15_l(
    width: float = Params_MMI2x2_85_15_L.default_width,
    width_taper: float = Params_MMI2x2_85_15_L.width_taper,
    length_taper: float = Params_MMI2x2_85_15_L.length_taper,
    length_mmi: float = Params_MMI2x2_85_15_L.length,
    width_mmi: float = Params_MMI2x2_85_15_L.width,
    gap_mmi: float = Params_MMI2x2_85_15_L.gap,
    cross_section: CrossSectionSpec = xs['strip'],
) -> gf.Component:
    """An mmi2x2 85/15 (L-Band).

    An asymmetric 2x2 splitter with 85/15 power split ratio

    Args:
        width: the width of the waveguides connecting at the mmi ports
        width_taper: the width at the base of the mmi body
        length_taper: the length of the tapers going towards the mmi body
        length_mmi: the length of the mmi body
        width_mmi: the width of the mmi body
        gap_mmi: the gap between the tapers at the mmi body
        cross_section: a cross section or its name or a function generating a cross section.
    """
    return _mmi2x2_with_sbends(
        width=width,
        width_taper=width_taper,
        length_taper=length_taper,
        length_mmi=length_mmi,
        width_mmi=width_mmi,
        gap_mmi=gap_mmi,
        cross_section=cross_section,
    )


@gf.cell
def mmi2x2_85_15_s(
    width: float = Params_MMI2x2_85_15_S.default_width,
    width_taper: float = Params_MMI2x2_85_15_S.width_taper,
    length_taper: float = Params_MMI2x2_85_15_S.length_taper,
    length_mmi: float = Params_MMI2x2_85_15_S.length,
    width_mmi: float = Params_MMI2x2_85_15_S.width,
    gap_mmi: float = Params_MMI2x2_85_15_S.gap,
    cross_section: CrossSectionSpec = xs['strip'],
) -> gf.Component:
    """An mmi2x2 85/15 (S-Band).

    An asymmetric 2x2 splitter with 85/15 power split ratio

    Args:
        width: the width of the waveguides connecting at the mmi ports
        width_taper: the width at the base of the mmi body
        length_taper: the length of the tapers going towards the mmi body
        length_mmi: the length of the mmi body
        width_mmi: the width of the mmi body
        gap_mmi: the gap between the tapers at the mmi body
        cross_section: a cross section or its name or a function generating a cross section.
    """
    return _mmi2x2_with_sbends(
        width=width,
        width_taper=width_taper,
        length_taper=length_taper,
        length_mmi=length_mmi,
        width_mmi=width_mmi,
        gap_mmi=gap_mmi,
        cross_section=cross_section,
    )


if __name__ == "__main__":
    c = mmi2x2_s()
    c.show()
