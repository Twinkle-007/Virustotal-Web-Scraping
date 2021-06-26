from selenium import webdriver
import time
import os
import json
import configparser
config = configparser.ConfigParser(delimiters=(':'))
config.optionxform = str
config.read('whitelist.cfg')

config.items("FILETYPES")
dict(config.items("FILETYPES")).keys()
#print(dict(config.items("FILETYPES")).keys())
#exit(1)

all_logs = os.listdir("./database/")

with open("verifications.json", 'r') as not_verified_holder:
    not_verified_files = json.load(not_verified_holder)

not_verified = not_verified_files['not_verified']



whitelisted_extension = list(dict(config.items("FILETYPES")).keys())

for log in all_logs:
    ext = log.split(".")
    ext = ext[1]
    if ext not in whitelisted_extension:
        not_verified.append(log)
    

with open("verifications.json", 'w') as new_data_not_verified:
    json.dump(not_verified_files, new_data_not_verified)

options = webdriver.ChromeOptions()
options.add_argument('headless')

driver = webdriver.Chrome(executable_path='./chromedriver', options=options)
driver.maximize_window()

with open("verifications.json", 'r') as not_verified_holder:
    not_verified_files = json.load(not_verified_holder)

not_verified = not_verified_files['not_verified']

reverser = 3

for item in reversed(not_verified):

    driver.get('https://www.virustotal.com/gui/')

    time.sleep(2)

    def expand_shadow_element(element):
        shadow_root = driver.execute_script(
            'return arguments[0].shadowRoot', element)
        return shadow_root

    shadow_section = expand_shadow_element(
        driver.find_element_by_tag_name("home-view"))
    upload_shadow = expand_shadow_element(
        shadow_section.find_element_by_tag_name("vt-ui-main-upload-form"))
    upload_shadow.find_element_by_id(
        'fileSelector').send_keys(f"{os.getcwd()}/database/{item}")

    time.sleep(1)

    try:
        upload_shadow.find_element_by_id('confirmUpload').click()
    except Exception as e:
        print(e)

    
    time.sleep(4)

    try:
        main_shell = expand_shadow_element(
            driver.find_element_by_tag_name("vt-ui-shell"))
        file_shell = expand_shadow_element(
            driver.find_element_by_tag_name("file-view"))
        report_shell = expand_shadow_element(
            file_shell.find_element_by_tag_name("vt-ui-main-generic-report"))
        detection_list_shell = expand_shadow_element(
            file_shell.find_element_by_tag_name("vt-ui-detections-list"))
        card_shell = expand_shadow_element(
            file_shell.find_element_by_tag_name("vt-ui-file-card"))
        generic_card_shell = expand_shadow_element(
            card_shell.find_element_by_tag_name("vt-ui-generic-card"))

        detection = card_shell.find_element_by_class_name(
            'detections').find_element_by_tag_name('p').text

        engines = detection_list_shell.find_elements_by_class_name('engine-name')
        about = detection_list_shell.find_elements_by_class_name(
            'individual-detection')
    except:
        time.sleep(50)
        try:
            main_shell = expand_shadow_element(
                driver.find_element_by_tag_name("vt-ui-shell"))
            file_shell = expand_shadow_element(
                driver.find_element_by_tag_name("file-view"))
            report_shell = expand_shadow_element(
                file_shell.find_element_by_tag_name("vt-ui-main-generic-report"))
            detection_list_shell = expand_shadow_element(
                file_shell.find_element_by_tag_name("vt-ui-detections-list"))
            card_shell = expand_shadow_element(
                file_shell.find_element_by_tag_name("vt-ui-file-card"))
            generic_card_shell = expand_shadow_element(
                card_shell.find_element_by_tag_name("vt-ui-generic-card"))

            detection = card_shell.find_element_by_class_name(
                'detections').find_element_by_tag_name('p').text

            engines = detection_list_shell.find_elements_by_class_name('engine-name')
            about = detection_list_shell.find_elements_by_class_name(
                'individual-detection')
        except:
            time.sleep(60)
            main_shell = expand_shadow_element(
                driver.find_element_by_tag_name("vt-ui-shell"))
            file_shell = expand_shadow_element(
                driver.find_element_by_tag_name("file-view"))
            report_shell = expand_shadow_element(
                file_shell.find_element_by_tag_name("vt-ui-main-generic-report"))
            detection_list_shell = expand_shadow_element(
                file_shell.find_element_by_tag_name("vt-ui-detections-list"))
            card_shell = expand_shadow_element(
                file_shell.find_element_by_tag_name("vt-ui-file-card"))
            generic_card_shell = expand_shadow_element(
                card_shell.find_element_by_tag_name("vt-ui-generic-card"))

            detection = card_shell.find_element_by_class_name(
                'detections').find_element_by_tag_name('p').text

            engines = detection_list_shell.find_elements_by_class_name('engine-name')
            about = detection_list_shell.find_elements_by_class_name(
                'individual-detection')   

    print("Verifying.....")
    print(f"{detection}\n")

    with open("/var/www/html/results.json", 'r') as result_getter:
        results_required = json.load(result_getter)

    container_required = results_required['results']

    data = { item: {
            "detection": detection,
            "antivirus-detections": {

            }
        }
    }

    containers_data = data[item]
    containers_data = containers_data['antivirus-detections']

    for engine, info in zip(engines, about):
        print(f"{engine.text} - {info.text}")
        containers_data[engine.text] = info.text

    container_required.append(data)

    print("")

    with open("/var/www/html/results.json", 'w') as result_container:
        json.dump(results_required, result_container)

    not_verified.remove(item)

    with open("verifications.json", 'w') as new_data_not_verified:
        json.dump(not_verified_files, new_data_not_verified)   

driver.quit()
