from opentrons import protocol_api

### metadata
metadata = {
    'apiLevel': '2.19',
    'protocolName': 'DNAmaker UDHR - Opentrons software calibration check',
    'description': 'FOR CALIBRATION CHECK ON OT-2 SOFTWARE ONLY',
    'author': 'Julien Leblanc'
    }


### requirements
requirements = {"robotType": "OT-2"}

# Create a json library which defined the numbers of pipettes and mounting positions:
    #-> to be used as values in protocol functions, we need to calculate them before + print help to check the values.
def get_values(*names):
    import json
    _all_values = json.loads("""{"p300_single_gen2_mount":"left","p20_single_gen2_mount":"right"}""")
    return [_all_values[n] for n in names]
result = get_values("p300_single_gen2_mount", "p20_single_gen2_mount")
p300_single_gen2_mount, p20_single_gen2_mount = result
print(f"p300_single_gen2_mount: {p300_single_gen2_mount}, p20_single_gen2_mount: {p20_single_gen2_mount}")


def run(ctx: protocol_api.ProtocolContext):

#|LOADING HARDWARE MODULES|#
    tc_mod = ctx.load_module('thermocyclerModuleV2') # USB position 1
    temp_mod_pos03 = ctx.load_module('temperature module gen2', 3) # USB position 2
    temp_mod_pos09 = ctx.load_module('temperature module gen2', 4) # USB position 3

#|LOADING LABWARE ON HARDWARE MODULES|#
    tc_plate = tc_mod.load_labware("nest_96_wellplate_100ul_pcr_full_skirt")
    aluminumblock_nest_96_wellplate_100ul_pos03_from_fridge = temp_mod_pos03.load_labware("opentrons_96_aluminumblock_nest_wellplate_100ul")
    aluminumblock_nest_24_500µL_pos09 = temp_mod_pos09.load_labware("opentrons_24_aluminumblock_nest_0.5ml_screwcap")
    trash = ctx.fixed_trash

#|LOADING TIP RACKS|#
    tipracks_p300_slot01 = ctx.load_labware('opentrons_96_filtertiprack_200ul', 1)
    tipracks_p20_slot02 = ctx.load_labware('opentrons_96_filtertiprack_20ul', 2)
    tipracks_p20_slot05 = ctx.load_labware('opentrons_96_filtertiprack_200ul', 5)


#|LOADING PIPETTES|#
    p300 = ctx.load_instrument('p300_single_gen2', p300_single_gen2_mount, tip_racks=[tipracks_p300_slot01])
    p300.default_speed = 200 # set pipette speed at 200 mm/s
    p300.flow_rate.aspirate = 50 # set aspiration flow rate speed at 50 µL/s
    p300.flow_rate.dispense = 50 # set distribution flow rate speed at 50 µL/s
    p300.flow_rate.blow_out = 10 # set blow rate at 10 µL/s

    p20 = ctx.load_instrument('p20_single_gen2', p20_single_gen2_mount, tip_racks=[tipracks_p20_slot05, tipracks_p20_slot02])
    p20.default_speed = 200
    p20.flow_rate.aspirate = 4
    p20.flow_rate.dispense = 4
    p20.flow_rate.blow_out = 4



###||PROTOCOLS||###

#must be home before running 
#    protocol.home()

    p20.pick_up_tip()
    p20.drop_tip()
    p300.pick_up_tip()
    p300.drop_tip()
