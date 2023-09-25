# -*- coding:utf-8 -*-
'''
Based on the 'state_changed.py' file, this file returns appropriate utterances for the game situation.
('state_changed.py' -> 'parse_tree.py' (current file) -> 'tts.py'

Order :
Phase / Hunger / Health / Sanity / Equipment / Attaking something / Attacked by something / Food
Tool / Making Lights / Nearby Lights / Monsters / Generic expression
'''
import ast
import re
import threading
import time

from Working_code import config as cf
from Working_code import tts

# set logger
logger = cf.logging.getLogger("__parser__")

# Randomly choose utterances from 'en-US/ko-KR_utterances.txt' files
def get_utterance_from_abstract(abstract):
    # return selected utterance only if current score is lower than 'CHATTINESS' placeholder
    if cf.priority_utterance_score[abstract] <= cf.CHATTINESS:
        # Evaluating safely the called utterance from the config file and get utterances as a list
        utt_list = ast.literal_eval(cf.RESPONSE_UTTS[abstract])
        selected_utt = utt_list[cf.last_index[abstract]%len(utt_list)]

        return selected_utt

    # If the score is higher, then pass
    else:
        pass


# Set up Repetition Delay. Based on the cf.REP_DELAY_AMT, If utterances print out third times, silent for 3 seconds
def repetition_delay(text):
    cf.LOCAL_REP_DELAY_AMT = cf.LOCAL_REP_DELAY_AMT - 1   # Reducing 1 'LOCAL_REP_DELAY_AMT' number

    cf.rep_delay_states[text] = cf.LOCAL_REP_DELAY_AMT    # Change 'rep_delay_states' to current 'LOCAL_REP_DELAY_AMT'

    # if 0, silent for 3 seconds
    if cf.rep_delay_states[text] == 0:
        time.sleep(3)

    # If 'LOCAL_REP_DELAY_AMT' is 0, reset the number using 'REP_DELAY_AMT'
    if cf.LOCAL_REP_DELAY_AMT == 0:
        cf.LOCAL_REP_DELAY_AMT = cf.REP_DELAY_AMT



# Return designated utterance for the appropriate situation
def parse_day_subtree(current_state, initial_state):
    ###############################################################################################
    # Phase starts
    # Phase - Day
    if current_state['Phase'] == 'day':
        cf.status['Phase'].append(current_state['Phase'])

        action = 'day'
        
        utterance = get_utterance_from_abstract('inform_morning')

        # If it is the first one, speak
        if len(cf.status['Phase']) == 1:
            tts.synthesize_utt(utterance, 'self')
            cf.last_index['inform_morning'] += 1

        # If it is not the first one, just speak when there's difference occurs
        elif len(cf.status['Phase']) > 1:
            if cf.status['Phase'][-2] != cf.status['Phase'][-1]:
                tts.synthesize_utt(utterance, 'self')
                cf.last_index['inform_morning'] += 1

    # Phase - Dusk
    elif current_state['Phase'] == 'dusk':
        cf.status['Phase'].append(current_state['Phase'])

        action = 'dusk'
        utterance = get_utterance_from_abstract('inform_evening')

        # If it is the first one, speak
        if len(cf.status['Phase']) == 1:
            tts.synthesize_utt(utterance, 'self')
            cf.last_index['inform_evening'] += 1

        # If it is not the first one, just speak when there's difference occurs
        elif len(cf.status['Phase']) > 1:
            if cf.status['Phase'][-2] != cf.status['Phase'][-1]:
                tts.synthesize_utt(utterance, 'self')
                cf.last_index['inform_evening'] += 1

    # Phase - Night
    elif current_state['Phase'] == 'night':
        cf.status['Phase'].append(current_state['Phase'])

        action = 'night'
        utterance = get_utterance_from_abstract('inform_night')

        # If it is the first one, speak
        if len(cf.status['Phase']) == 1:
            tts.synthesize_utt(utterance, 'self')
            cf.last_index['inform_night'] += 1

        # If it is not the first one, just speak when there's difference occurs
        elif len(cf.status['Phase']) > 1:
            if cf.status['Phase'][-2] != cf.status['Phase'][-1]:
                tts.synthesize_utt(utterance, 'self')
                cf.last_index['inform_night'] += 1
    # Phase ends
    ###############################################################################################


    ###############################################################################################
    # Hunger starts
    # Hunger - very low
    if int(float(current_state['Hunger_AVATAR'])) < cf.STARVING:
        cf.status['Hunger_AVATAR'].append(int(float(current_state['Hunger_AVATAR'])))

        action = 'hunger_is_dangerous'
        utterance = get_utterance_from_abstract('inform_starving')

        # If it is the first one, speak
        if len(cf.status['Hunger_AVATAR']) == 1:
            tts.synthesize_utt(utterance, 'self')
            cf.last_index['inform_starving'] += 1

        # If it is not the first one, just speak like below situation
        elif len(cf.status['Hunger_AVATAR']) > 1:
            # When there's difference occurs and 'Hunger' status is bigger than 25, then speak
            if cf.status['Hunger_AVATAR'][-2] < cf.status['Hunger_AVATAR'][-1] and cf.status['Hunger_AVATAR'][-1] > 25:
                tts.synthesize_utt(utterance, 'self')
                cf.last_index['inform_starving'] += 1

            # If the Hunger status is 29, to reduce a bit of repetition (30->29->30->29),
            # Only speaks when the just before the latest one is 29
            elif cf.status['Hunger_AVATAR'][-2] == 29 and cf.status['Hunger_AVATAR'][-1] != 29:
                tts.synthesize_utt(utterance, 'self')
                cf.last_index['inform_starving'] += 1

    # Hunger - low
    elif cf.HUNGRY >= int(float(current_state['Hunger_AVATAR'])) > cf.STARVING:
        cf.status['Hunger_AVATAR'].append(int(float(current_state['Hunger_AVATAR'])))

        action = 'hunger_is_quite_low'
        utterance = get_utterance_from_abstract('inform_hunger') # en

        # If it is the first one, speak
        if len(cf.status['Hunger_AVATAR']) == 1:
            tts.synthesize_utt(utterance, 'self')
            cf.last_index['inform_hunger'] += 1

        # If it is not the first one and if the Hunger status is 31 ~ 45, speak when there's difference occurs
        elif len(cf.status['Hunger_AVATAR']) > 1:
            if cf.status['Hunger_AVATAR'][-2] < cf.status['Hunger_AVATAR'][-1] and cf.status['Hunger_AVATAR'][-1] > 45:
                tts.synthesize_utt(utterance, 'self')
                cf.last_index['inform_hunger'] += 1
    # Hunger ends
    ###############################################################################################


    ###############################################################################################
    # Health starts
    # Health - very low
    if int(float(current_state['Health_AVATAR'])) < cf.DYING:
        cf.status['Health_AVATAR'].append(int(float(current_state['Health_AVATAR'])))

        action = 'Almost_Dying'
        utterance = get_utterance_from_abstract('inform_dying')  # en

        # If it is the first one, speak
        if len(cf.status['Health_AVATAR']) == 1:
            tts.synthesize_utt(utterance, 'self')
            cf.last_index['inform_dying'] += 1

        # If it is not the first one, just speak like below situation
        elif len(cf.status['Health_AVATAR']) > 1:
            # When there's difference occurs and 'Health' status is bigger than 25, then speak
            if cf.status['Health_AVATAR'][-2] < cf.status['Health_AVATAR'][-1] and cf.status['Health_AVATAR'][-1] > 25:
                tts.synthesize_utt(utterance, 'self')
                cf.last_index['inform_dying'] += 1

            # If the Health status is 29, to reduce a bit of repetition (30->29->30->29),
            # Only speaks when the just before the latest one is 29
            elif cf.status['Health_AVATAR'][-2] == 29 and cf.status['Health_AVATAR'][-1] != 29:
                tts.synthesize_utt(utterance, 'self')
                cf.last_index['inform_dying'] += 1

    # Health - low
    elif cf.INJURED > int(float(current_state['Health_AVATAR'])) > cf.DYING:
        cf.status['Health_AVATAR'].append(int(float(current_state['Health_AVATAR'])))

        action = 'Quite_injured'
        utterance = get_utterance_from_abstract('inform_injured') # en

        # If it is the first one, speak
        if len(cf.status['Health_AVATAR']) == 1:
            tts.synthesize_utt(utterance, 'self')
            cf.last_index['inform_injured'] += 1

        # If it is not the first one and if the Health status is 31 ~ 45, speak when there's difference occurs
        elif len(cf.status['Health_AVATAR']) > 1:
            if cf.status['Health_AVATAR'][-2] < cf.status['Health_AVATAR'][-1] and cf.status['Health_AVATAR'][-1] > 45:
                tts.synthesize_utt(utterance, 'self')
                cf.last_index['inform_injured'] += 1
    # Health ends
    ###############################################################################################


    ###############################################################################################
    # Sanity starts
    # Sanity - Very low
    if int(float(current_state['Sanity_AVATAR'])) < cf.SANITY_DANGER:
        cf.status['Sanity_AVATAR'].append(int(float(current_state['Sanity_AVATAR'])))

        action = 'Mental_Crushed'
        utterance = get_utterance_from_abstract('inform_getting_insane') # en # en

        # If it is the first one, speak
        if len(cf.status['Sanity_AVATAR']) == 1:
            tts.synthesize_utt(utterance, 'self')
            cf.last_index['inform_getting_insane'] += 1

        # If it is not the first one, just speak like below situation
        elif len(cf.status['Sanity_AVATAR']) > 1:
            # When there's difference occurs and 'Sanity' status is bigger than 25, then speak
            if cf.status['Sanity_AVATAR'][-2] < cf.status['Sanity_AVATAR'][-1] and cf.status['Sanity_AVATAR'][-1] > 25:
                tts.synthesize_utt(utterance, 'self')
                cf.last_index['inform_getting_insane'] += 1

            # If the Sanity status is 29, to reduce a bit of repetition (30->29->30->29),
            # Only speaks when the just before the latest one is 29
            elif cf.status['Sanity_AVATAR'][-2] == 29 and cf.status['Sanity_AVATAR'][-1] != 29:
                tts.synthesize_utt(utterance, 'self')
                cf.last_index['inform_getting_insane'] += 1

    # Sanity - low
    elif cf.SANITY_LOW > int(float(current_state['Sanity_AVATAR'])) > cf.SANITY_DANGER :
        cf.status['Sanity_AVATAR'].append(int(float(current_state['Sanity_AVATAR'])))

        action = 'Quite_crushed'
        utterance = get_utterance_from_abstract('inform_low_sanity')  # en

        # If it is the first one, speak
        if len(cf.status['Sanity_AVATAR']) == 1:
            tts.synthesize_utt(utterance, 'self')
            cf.last_index['inform_low_sanity'] += 1

        # If it is not the first one and if the Sanity status is 31 ~ 45, speak when there's difference occurs
        elif len(cf.status['Sanity_AVATAR']) > 1:
            if cf.status['Sanity_AVATAR'][-2] < cf.status['Sanity_AVATAR'][-1] and cf.status['Sanity_AVATAR'][-1] > 45:
                tts.synthesize_utt(utterance, 'self')
                cf.last_index['inform_low_sanity'] += 1
    # Sanity ends
    ###############################################################################################


    ###############################################################################################
    # Equipment starts
    # Current Equipment
    if current_state['Curr_Equip_Hands_AVATAR'] != 'nil':
        cf.status['Curr_Equip_Hands_AVATAR'].append(current_state['Curr_Equip_Hands_AVATAR'])

        action = 'Equip_a_tool_to_use'

        # bring the current equipment (format is like '125516 - axe(LIMBO)')
        string = cf.status['Curr_Equip_Hands_AVATAR'][-1]

        # Strip just words from the current equipment
        equip_result = re.findall('[a-z]+', string)

        if len(equip_result) != 1:
            logger.error('equipment list length is not 1')

        # format current equipment as string type
        equip_result = str(equip_result[0])
        
        # write at the log file
        logger.debug('equipment found ' + equip_result)
        logger.info('equipping with ' + equip_result)

        # bring utterances from data/*_utterances.txt
        utterance = get_utterance_from_abstract('inform_equip')

        # If utterance contains 'something', then change this to current equipment name
        if "something" in utterance:
            if cf.THIS_LANGUAGE == 'ko-KR':
                try:    
                    equip_result = cf.CONV_UTTS[equip_result]
                except:
                    pass
            utterance = utterance.replace("something", equip_result)

        # If it is the first one, speak
        if len(cf.status['Curr_Equip_Hands_AVATAR']) == 1:
            tts.synthesize_utt(utterance, 'self')
            cf.last_index['inform_equip'] += 1

        # If it is not the first one, just speak when there's difference occurs
        elif len(cf.status['Curr_Equip_Hands_AVATAR']) > 1:
            if cf.status['Curr_Equip_Hands_AVATAR'][-2] != cf.status['Curr_Equip_Hands_AVATAR'][-1]:
                # Apply repetition delay function for current category (The function starts at line 28)
                repetition_delay('Curr_Equip_Hands_AVATAR')

                # If the rep_delay_states number(count) is not 0, then utterances keep coming out
                if cf.rep_delay_states['Curr_Equip_Hands_AVATAR'] != 0:
                    tts.synthesize_utt(utterance, 'self')
                    cf.last_index['inform_equip'] += 1
    # Equipment ends
    ###############################################################################################


    ###############################################################################################
    # Attack starts
    # Attacking Something
    if current_state['Attack_Target_AVATAR'] != 'nil':
        cf.status['Attack_Target_AVATAR'].append(current_state['Attack_Target_AVATAR'])

        action = 'Attack'

        # bring the current attacking thing (format is like '124017 - tallbird')
        string = cf.status['Attack_Target_AVATAR'][-1]

        # Strip just words from current attacking thing
        attack_result = re.findall('[a-z]+', string)

        if len(attack_result) != 1:
            logger.error('attack list length is not 1')

        # format current attacking thing as string type
        attack_result = str(attack_result[0])

        # write at the log file
        logger.debug('attack found ' + attack_result)
        logger.info('attack ' + attack_result)

        utterance = get_utterance_from_abstract('inform_attack')

        # If utterance contains 'something', then change this to current attacking thing's name
        if "something" in utterance:
            if cf.THIS_LANGUAGE == 'ko-KR':
                try:
                    attack_result = cf.CONV_UTTS[attack_result]
                except:
                    pass
            utterance = utterance.replace("something", attack_result)

        # If it is the first one, speak
        if len(cf.status['Attack_Target_AVATAR']) == 1:
            tts.synthesize_utt(utterance, 'self')
            cf.last_index['inform_attack'] += 1

        # If it is not the first one, just speak when there's difference occurs
        elif len(cf.status['Attack_Target_AVATAR']) > 1:
            if cf.status['Attack_Target_AVATAR'][-2] != cf.status['Attack_Target_AVATAR'][-1]:
                # Apply repetition delay function for current category (The function starts at line 28)
                repetition_delay('Attack_Target_AVATAR')

                # If the rep_delay_states number(count) is not 0, then utterances keep coming out
                if cf.rep_delay_states['Attack_Target_AVATAR'] != 0:
                    tts.synthesize_utt(utterance, 'self')
                    cf.last_index['inform_attack'] += 1
    # Attack ends
    ###############################################################################################

    ###############################################################################################
    # Defense starts
    # Being Attacked by something
    if current_state['Defense_Target_AVATAR'] != 'nil':
        cf.status['Defense_Target_AVATAR'].append(current_state['Defense_Target_AVATAR'])

        action = 'Attacked'

        # bring the current being attacked thing (format is like '124017 - tallbird')
        string = cf.status['Defense_Target_AVATAR'][-1]

        # Strip just words from current being attacked thing
        defense_result = re.findall('[a-z]+', string)

        if len(defense_result) != 1:
            logger.error('defense list length is not 1')

        # format current being attacked thing as string type
        defense_result = str(defense_result[0])

        # write at the log file
        logger.debug('defense found ' + defense_result)
        logger.info('being attacked by ' + defense_result)

        utterance = get_utterance_from_abstract('inform_defense')

        # If utterance contains 'something', then change this to current being attacked thing's name
        if "something" in utterance:
            if cf.THIS_LANGUAGE == 'ko-KR':
                try:
                    defense_result = cf.CONV_UTTS[defense_result]
                except:
                    pass
            utterance = utterance.replace("something", defense_result)

        # If it is the first one, speak
        if len(cf.status['Defense_Target_AVATAR']) == 1:
            tts.synthesize_utt(utterance, 'self')
            cf.last_index['inform_defense'] += 1

        # If it is not the first one, just speak when there's difference occurs
        elif len(cf.status['Defense_Target_AVATAR']) > 1:
            if cf.status['Defense_Target_AVATAR'][-2] != cf.status['Defense_Target_AVATAR'][-1]:
                # Apply repetition delay function for current category (The function starts at line 28)
                repetition_delay('Defense_Target_AVATAR')

                # If the rep_delay_states number(count) is not 0, then utterances keep coming out
                if cf.rep_delay_states['Defense_Target_AVATAR'] != 0:
                    tts.synthesize_utt(utterance, 'self')
                    cf.last_index['inform_defense'] += 1
    # Defense ends
    ###############################################################################################

    ###############################################################################################
    # Food starts
    # Starting : Food
    # if current_state['Food_AVATAR'] == 'No Food!':
    #     cf.status['Food_AVATAR'].append(current_state['Food_AVATAR'])
    #
    #     action = 'Food_is_needed_immediately'
    #     utterance = get_utterance_from_abstract('inform_no_food')
    #     # utterance = "We have no food now." # en
    #
    #     if len(cf.status['Food_AVATAR']) == 1:
    #         tts.synthesize_utt(utterance)
    #     elif len(cf.status['Food_AVATAR']) > 1:
    #         if cf.status['Food_AVATAR'][-2] != cf.status['Food_AVATAR'][-1]:
    #             tts.synthesize_utt(utterance)

    # Food is not enough
    if current_state['Food_AVATAR'] > 50:    # Fine!
        cf.status['Food_AVATAR'].append(current_state['Food_AVATAR'])

        action = 'Food_is_sufficient'
        utterance = get_utterance_from_abstract('inform_enough_food')

        # If it is the first one, speak
        if len(cf.status['Food_AVATAR']) == 1:
            tts.synthesize_utt(utterance, 'self')
            cf.last_index['inform_enough_food'] += 1

        # If it is not the first one, just speak when there's difference occurs
        elif len(cf.status['Food_AVATAR']) > 1:
            if cf.status['Food_AVATAR'][-2] != cf.status['Food_AVATAR'][-1]:
                # Apply repetition delay function for current category (The function starts at line 28)
                repetition_delay('Food_AVATAR')

                # If the rep_delay_states number(count) is not 0, then utterances keep coming out
                if cf.rep_delay_states['Food_AVATAR'] != 0:
                    tts.synthesize_utt(utterance, 'self')
                    cf.last_index['inform_enough_food'] += 1

    # Food is not enough
    elif current_state['Food_AVATAR'] > 0:      #Less Food!
        cf.status['Food_AVATAR'].append(current_state['Food_AVATAR'])

        action = 'Food_is_needed'
        utterance = get_utterance_from_abstract('inform_less_food')

        # If it is the first one, speak
        if len(cf.status['Food_AVATAR']) == 1:
            tts.synthesize_utt(utterance, 'self')
            cf.last_index['inform_less_food'] += 1

        # If it is not the first one, just speak when there's difference occurs
        elif len(cf.status['Food_AVATAR']) > 1:
            if cf.status['Food_AVATAR'][-2] != cf.status['Food_AVATAR'][-1]:
                # Apply repetition delay function for current category (The function starts at line 28)
                repetition_delay('Food_AVATAR')

                # If the rep_delay_states number(count) is not 0, then utterances keep coming out
                if cf.rep_delay_states['Food_AVATAR'] != 0:
                    tts.synthesize_utt(utterance, 'self')
                    cf.last_index['inform_less_food'] += 1
    # Food ends
    ###############################################################################################

    ###############################################################################################
    # Tool starts
    # Tools(Resources) - Less resources
    # if current_state['Tool_AVATAR'] == 'Less resources':
    #     cf.status['Tool_AVATAR'].append(current_state['Tool_AVATAR'])
    #
    #     action = 'resources_are_needed_for_tools'
    #     utterance = get_utterance_from_abstract('inform_no_resources_tool')
    #     # utterance = "Need more to make tools!" # en
    #
    #     if len(cf.status['Tool_AVATAR']) == 1:
    #         tts.synthesize_utt(utterance)
    #     elif len(cf.status['Tool_AVATAR']) > 1:
    #         if cf.status['Tool_AVATAR'][-2] != cf.status['Tool_AVATAR'][-1]:
    #             tts.synthesize_utt(utterance)

    # Tools(Resources) - both possible
    if current_state['Twigs_AVATAR'] >= 3 and current_state['Flint_AVATAR'] >= 3:
        cf.status['Twigs_AVATAR'].append(current_state['Twigs_AVATAR'])
        cf.status['Flint_AVATAR'].append(current_state['Flint_AVATAR'])

        action = 'Tools_could_be_made'
        utterance = get_utterance_from_abstract('inform_both')
        
        # If it is the first one, speak
        if len(cf.status['Twigs_AVATAR']) == 1:
            tts.synthesize_utt(utterance, 'self')
            cf.last_index['inform_both'] += 1

        # If it is not the first one, just speak when there's difference occurs
        elif len(cf.status['Twigs_AVATAR']) > 1:
            if cf.status['Twigs_AVATAR'][-2] != cf.status['Twigs_AVATAR'][-1] and \
                cf.status['Flint_AVATAR'][-2] != cf.status['Flint_AVATAR'][-1]:
                    # Apply repetition delay function for current category (The function starts at line 28)
                    repetition_delay('Tool_AVATAR')

                    # If the rep_delay_states number(count) is not 0, then utterances keep coming out
                    if cf.rep_delay_states['Tool_AVATAR'] != 0:
                        tts.synthesize_utt(utterance, 'self')
                        cf.last_index['inform_both'] += 1
                
    # Tools(Resources) - Pickaxe possible
    elif current_state['Twigs_AVATAR'] >= 2 and current_state['Flint_AVATAR'] >= 2:
        cf.status['Twigs_AVATAR'].append(current_state['Twigs_AVATAR'])
        cf.status['Flint_AVATAR'].append(current_state['Flint_AVATAR'])

        action = 'One_of_Axe_pickaxe_could_be_made'
        utterance = get_utterance_from_abstract('inform_axe_or_pickaxe')

        # If it is the first one, speak
        if len(cf.status['Twigs_AVATAR']) == 1:
            tts.synthesize_utt(utterance, 'self')
            cf.last_index['inform_axe_or_pickaxe'] += 1

        # If it is not the first one, just speak when there's difference occurs
        elif len(cf.status['Twigs_AVATAR']) > 1:
            if cf.status['Twigs_AVATAR'][-2] != cf.status['Twigs_AVATAR'][-1] and \
                cf.status['Flint_AVATAR'][-2] != cf.status['Flint_AVATAR'][-1]:
                    # Apply repetition delay function for current category (The function starts at line 28)
                    repetition_delay('Tool_AVATAR')

                    # If the rep_delay_states number(count) is not 0, then utterances keep coming out
                    if cf.rep_delay_states['Tool_AVATAR'] != 0:
                        tts.synthesize_utt(utterance, 'self')
                        cf.last_index['inform_axe_or_pickaxe'] += 1
                
    # Tools(Resources) - Axe possible
    elif current_state['Twigs_AVATAR'] >= 1 and current_state['Flint_AVATAR'] >= 1:
        cf.status['Twigs_AVATAR'].append(current_state['Twigs_AVATAR'])
        cf.status['Flint_AVATAR'].append(current_state['Flint_AVATAR'])

        action = 'Axe_could_be_made'
        utterance = get_utterance_from_abstract('inform_only_axe')

        # If it is the first one, speak
        if len(cf.status['Twigs_AVATAR']) == 1:
            tts.synthesize_utt(utterance, 'self')
            cf.last_index['inform_only_axe'] += 1

        # If it is not the first one, just speak when there's difference occurs
        elif len(cf.status['Twigs_AVATAR']) > 1:
            if cf.status['Twigs_AVATAR'][-2] != cf.status['Twigs_AVATAR'][-1] and \
                cf.status['Flint_AVATAR'][-2] != cf.status['Flint_AVATAR'][-1]:
                    # Apply repetition delay function for current category (The function starts at line 28)
                    repetition_delay('Tool_AVATAR')

                    # If the rep_delay_states number(count) is not 0, then utterances keep coming out
                    if cf.rep_delay_states['Tool_AVATAR'] != 0:
                        tts.synthesize_utt(utterance, 'self')
                        cf.last_index['inform_only_axe'] += 1
    # Tool ends
    ###############################################################################################

    ###############################################################################################
    # Making_light starts
    # Making Lights - Less resources
    # if current_state['Lights_AVATAR'] == 'Less resources' and current_state['Is_Light_AVATAR'] == 'No lights!':
    #     cf.status['Lights_AVATAR'].append(current_state['Lights_AVATAR'])
    #     cf.status['Is_Light_AVATAR'].append(current_state['Is_Light_AVATAR'])
    #
    #     action = 'resources_are_needed_for_lights'
    #     utterance = get_utterance_from_abstract('inform_no_resources_light')
    #     # utterance = "Need more resources to make a torch!" #en
    #
    #     if len(cf.status['Lights_AVATAR']) == 1:
    #         tts.synthesize_utt(utterance)
    #     elif len(cf.status['Lights_AVATAR']) > 1:
    #         if cf.status['Lights_AVATAR'][-2] != cf.status['Lights_AVATAR'][-1]:
    #             tts.synthesize_utt(utterance)
    
    # Making Lights - Firepit possible
    if current_state['Grass_AVATAR'] >= 2 and current_state['Log_AVATAR'] >= 2 and current_state['Twigs_AVATAR'] >= 2 and current_state['Rock_AVATAR'] >= 12 and current_state['Is_Light_AVATAR'] == 'nil':
        cf.status['Grass_AVATAR'].append(current_state['Grass_AVATAR'])
        cf.status['Log_AVATAR'].append(current_state['Log_AVATAR'])
        cf.status['Twigs_AVATAR'].append(current_state['Twigs_AVATAR'])
        cf.status['Rock_AVATAR'].append(current_state['Rock_AVATAR'])
        cf.status['Is_Light_AVATAR'].append(current_state['Is_Light_AVATAR'])
        
        action = 'resources_are_sufficient_to_make_fire_pit'
        utterance = get_utterance_from_abstract('inform_firepit')

        # If it is the first one, speak
        if len(cf.status['Grass_AVATAR']) == 1:
            tts.synthesize_utt(utterance, 'self')
            cf.last_index['inform_firepit'] += 1

        # If it is not the first one, just speak when there's difference occurs
        elif len(cf.status['Grass_AVATAR']) > 1:
            if cf.status['Grass_AVATAR'][-2] != cf.status['Grass_AVATAR'][-1] and \
                cf.status['Log_AVATAR'][-2] != cf.status['Log_AVATAR'][-1] and \
                    cf.status['Twigs_AVATAR'][-2] != cf.status['Twigs_AVATAR'][-1] and \
                        cf.status['Rock_AVATAR'][-2] != cf.status['Rock_AVATAR'][-1] and \
                            cf.status['Is_Light_AVATAR'][-2] != cf.status['Is_Light_AVATAR'][-1]:
                                # Apply repetition delay function for current category (The function starts at line 28)
                                repetition_delay('Lights_AVATAR')

                                # If the rep_delay_states number(count) is not 0, then utterances keep coming out
                                if cf.rep_delay_states['Lights_AVATAR'] != 0:
                                    tts.synthesize_utt(utterance, 'self')
                                    cf.last_index['inform_firepit'] += 1
                
    # Making Lights - Campfire possible
    elif current_state['Grass_AVATAR'] >= 3 and current_state['Log_AVATAR'] >= 2 and current_state['Twigs_AVATAR'] >= 2 and current_state['Is_Light_AVATAR'] == 'nil':
        cf.status['Grass_AVATAR'].append(current_state['Grass_AVATAR'])
        cf.status['Log_AVATAR'].append(current_state['Log_AVATAR'])
        cf.status['Twigs_AVATAR'].append(current_state['Twigs_AVATAR'])
        cf.status['Rock_AVATAR'].append(current_state['Rock_AVATAR'])
        cf.status['Is_Light_AVATAR'].append(current_state['Is_Light_AVATAR'])

        action = 'resources_are_sufficient_to_make_campfire'
        utterance = get_utterance_from_abstract('inform_campfire')

        # If it is the first one, speak
        if len(cf.status['Grass_AVATAR']) == 1:
            tts.synthesize_utt(utterance, 'self')
            cf.last_index['inform_campfire'] += 1

        # If it is not the first one, just speak when there's difference occurs
        elif len(cf.status['Grass_AVATAR']) > 1:
            if cf.status['Grass_AVATAR'][-2] != cf.status['Grass_AVATAR'][-1] and \
                cf.status['Log_AVATAR'][-2] != cf.status['Log_AVATAR'][-1] and \
                    cf.status['Twigs_AVATAR'][-2] != cf.status['Twigs_AVATAR'][-1] and \
                        cf.status['Is_Light_AVATAR'][-2] != cf.status['Is_Light_AVATAR'][-1]:
                            # Apply repetition delay function for current category (The function starts at line 28)
                            repetition_delay('Lights_AVATAR')

                            # If the rep_delay_states number(count) is not 0, then utterances keep coming out
                            if cf.rep_delay_states['Lights_AVATAR'] != 0:
                                tts.synthesize_utt(utterance, 'self')
                                cf.last_index['inform_campfire'] += 1
                            
    # Making Lights - only torch
    elif current_state['Grass_AVATAR'] >= 2 and current_state['Twigs_AVATAR'] >= 2 and current_state['Is_Light_AVATAR'] == 'nil':
        cf.status['Grass_AVATAR'].append(current_state['Grass_AVATAR'])
        cf.status['Log_AVATAR'].append(current_state['Log_AVATAR'])
        cf.status['Twigs_AVATAR'].append(current_state['Twigs_AVATAR'])
        cf.status['Rock_AVATAR'].append(current_state['Rock_AVATAR'])
        cf.status['Is_Light_AVATAR'].append(current_state['Is_Light_AVATAR'])

        action = 'resources_are_sufficient_to_make_torch'
        utterance = get_utterance_from_abstract('inform_torch')

        # If it is the first one, speak
        if len(cf.status['Grass_AVATAR']) == 1:
            tts.synthesize_utt(utterance, 'self')
            cf.last_index['inform_torch'] += 1

        # If it is not the first one, just speak when there's difference occurs
        elif len(cf.status['Grass_AVATAR']) > 1:
            if cf.status['Grass_AVATAR'][-2] != cf.status['Grass_AVATAR'][-1] and \
                cf.status['Twigs_AVATAR'][-2] != cf.status['Twigs_AVATAR'][-1] and \
                    cf.status['Is_Light_AVATAR'][-2] != cf.status['Is_Light_AVATAR'][-1]:
                        # Apply repetition delay function for current category (The function starts at line 28)
                        repetition_delay('Lights_AVATAR')

                        # If the rep_delay_states number(count) is not 0, then utterances keep coming out
                        if cf.rep_delay_states['Lights_AVATAR'] != 0:
                            tts.synthesize_utt(utterance, 'self')
                            cf.last_index['inform_torch'] += 1
    # Making_light ends
    ###############################################################################################


    ###############################################################################################
    # Nearby_light starts
    # Nearby lights - something is near
    if current_state['Is_Fireplace_AVATAR'] == "nil" and current_state['Is_Light_AVATAR'] != "nil" and str(current_state['Curr_Equip_Hands_AVATAR'][9:]) != 'torch(LIMBO)':
        cf.status['Is_Fireplace_AVATAR'].append(current_state['Is_Fireplace_AVATAR'])
        cf.status['Is_Light_AVATAR'].append(current_state['Is_Light_AVATAR'])
        cf.status['Curr_Equip_Hands_AVATAR'].append(current_state['Curr_Equip_Hands_AVATAR'])
        
        action = 'torch_is_nearby'
        utterance = get_utterance_from_abstract('inform_near_light')

        # If it is the first one, speak
        if len(cf.status['Is_Fireplace_AVATAR']) == 1:
            tts.synthesize_utt(utterance, 'self')
            cf.last_index['inform_near_light'] += 1

        # If it is not the first one, just speak when there's difference occurs
        elif len(cf.status['Is_Fireplace_AVATAR']) > 1:
            if cf.status['Is_Fireplace_AVATAR'][-2] != cf.status['Is_Fireplace_AVATAR'][-1] and \
                cf.status['Is_Light_AVATAR'][-2] != cf.status['Is_Light_AVATAR'][-1] and \
                    str(cf.status['Curr_Equip_Hands_AVATAR'][-2][9:]) != str(cf.status['Curr_Equip_Hands_AVATAR'][-1][9:]):
                        # Apply repetition delay function for current category (The function starts at line 28)
                        repetition_delay('Is_Light_AVATAR')

                        # If the rep_delay_states number(count) is not 0, then utterances keep coming out
                        if cf.rep_delay_states['Is_Light_AVATAR'] != 0:
                            tts.synthesize_utt(utterance, 'self')
                            cf.last_index['inform_near_light'] += 1
                

    # Nearby lights - Campfire/Firepit is near
    elif current_state['Is_Fireplace_AVATAR'] != "nil":
        cf.status['Is_Fireplace_AVATAR'].append(current_state['Is_Fireplace_AVATAR'])
        cf.status['Is_Light_AVATAR'].append(current_state['Is_Light_AVATAR'])
        cf.status['Curr_Equip_Hands_AVATAR'].append(current_state['Curr_Equip_Hands_AVATAR'])

        action = 'campfire_nearby'
        utterance = get_utterance_from_abstract('inform_near_campfire')

        # If it is the first one, speak
        if len(cf.status['Is_Fireplace_AVATAR']) == 1:
            tts.synthesize_utt(utterance, 'self')
            cf.last_index['inform_near_campfire'] += 1

        # If it is not the first one, just speak when there's difference occurs
        elif len(cf.status['Is_Fireplace_AVATAR']) > 1:
            if cf.status['Is_Fireplace_AVATAR'][-2] != cf.status['Is_Fireplace_AVATAR'][-1]:
                # Apply repetition delay function for current category (The function starts at line 28)
                repetition_delay('Is_Light_AVATAR')

                # If the rep_delay_states number(count) is not 0, then utterances keep coming out
                if cf.rep_delay_states['Is_Light_AVATAR'] != 0:
                    tts.synthesize_utt(utterance, 'self')
                    cf.last_index['inform_near_campfire'] += 1
    # Nearby_light ends
    ###############################################################################################

    ###############################################################################################
    # Monsters start
    # Monsters - a lot (more than 5)
    if current_state['Is_Monster_AVATAR'] > 5:
        cf.status['Is_Monster_AVATAR'].append(current_state['Is_Monster_AVATAR'])

        action = 'monsters_are_lot_nearby'
        utterance = get_utterance_from_abstract('inform_lots_of_monsters')

        # If it is the first one, speak
        if len(cf.status['Is_Monster_AVATAR']) == 1:
            tts.synthesize_utt(utterance, 'self')
            cf.last_index['inform_lots_of_monsters'] += 1

        # If it is not the first one, just speak when there's difference occurs
        elif len(cf.status['Is_Monster_AVATAR']) > 1:
            if cf.status['Is_Monster_AVATAR'][-2] != cf.status['Is_Monster_AVATAR'][-1]:
                # Apply repetition delay function for current category (The function starts at line 28)
                repetition_delay('Is_Monster_AVATAR')

                # If the rep_delay_states number(count) is not 0, then utterances keep coming out
                if cf.rep_delay_states['Is_Monster_AVATAR'] != 0:
                    tts.synthesize_utt(utterance, 'self')
                    cf.last_index['inform_lots_of_monsters'] += 1

    # Monsters - a few (less than 5)
    elif current_state['Is_Monster_AVATAR'] > 0:
        cf.status['Is_Monster_AVATAR'].append(current_state['Is_Monster_AVATAR'])

        action = 'some_monsters_are_nearby'
        utterance = get_utterance_from_abstract('inform_a_few_monsters')

        # If it is the first one, speak
        if len(cf.status['Is_Monster_AVATAR']) == 1:
            tts.synthesize_utt(utterance, 'self')
            cf.last_index['inform_a_few_monsters'] += 1

        # If it is not the first one, just speak when there's difference occurs
        elif len(cf.status['Is_Monster_AVATAR']) > 1:
            if cf.status['Is_Monster_AVATAR'][-2] != cf.status['Is_Monster_AVATAR'][-1]:
                # Apply repetition delay function for current category (The function starts at line 28)
                repetition_delay('Is_Monster_AVATAR')

                # If the rep_delay_states number(count) is not 0, then utterances keep coming out
                if cf.rep_delay_states['Is_Monster_AVATAR'] != 0:
                    tts.synthesize_utt(utterance, 'self')
                    cf.last_index['inform_a_few_monsters'] += 1
    # Monsters end
    ###############################################################################################

    ###############################################################################################
    # Action suggestion starts
    # Action Suggestions
    # Works 'Player_Xloc' is not 'nil' ('nil' means that the player does not participate at the current game)
    if current_state['Player_Xloc'] != 'nil':
        cf.status['Player_Xloc'].append(float(current_state['Player_Xloc']))
        
        # At night, the movement is limited, so It works only for 'day' and 'dusk' phase
        if cf.status['Phase'][-1] == 'day' or cf.status['Phase'][-1] == 'dusk':
            # if player's location is same for 25 rows, then speak utterance
            if len(cf.status['Player_Xloc']) >= 25:
                if cf.status['Player_Xloc'][-1] == cf.status['Player_Xloc'][-25]:
                    action = 'No_movements_for_a_while'
                    utterance = get_utterance_from_abstract('inform_generic_expression')
                    tts.synthesize_utt(utterance, 'self')
                    cf.last_index['inform_generic_expression'] += 1
                    del(cf.status['Player_Xloc'])
                else:
                    pass
    # Action suggestion ends
    ###############################################################################################
    '''
    ***
    add stuff here
    ***
    '''
    return utterance



def parse_decision_tree(current_state, initial_state):
    '''
    parse the decision tree to find the right action for the current state
    synthesize the utterance and play it back
    '''
    # Set up action and utterance as None
    action = None
    utterance = None
    self_asr_check = None

    # If the current state 'Phase' comes as an input then send the state to 'parse_day_subtree()' function
    if current_state['Phase'] == 'day' or current_state['Phase'] == 'dusk' or current_state['Phase'] == 'night':
        logger.info(' parse day tree ')
        parse_day_subtree(current_state, initial_state)

    # If other state comes as an input, write down to the log file
    else:
        logger.error(' no daytime info available ')

    # Set the thread and start
    t_synth = threading.Thread(target=tts.synthesize_utt, args=[utterance, self_asr_check], daemon=True)
    t_synth.start()
    # t_synth.join()