def local_phone(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    phone_file = open('local_phone.txt', 'w', encoding='utf-8')
    rest_file = open('rest_info.txt', 'w', encoding='utf-8')
    for line in lines:
        space = line.find(' ')

        number = line[:space]
        rest = line[space + 1:]
        if number:
            phone_file.writelines(number)
            phone_file.writelines('\n')
        rest_file.writelines(rest)

    phone_file.close()
    rest_file.close()


def mobile_phone(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    mobile_file = open('mobile_phone.txt', 'w', encoding='utf-8')
    rest_file = open('rest_name.txt', 'w', encoding='utf-8')
    for line in lines:
        space = line.find(' ')

        number = line[:space]
        rest = line[space:]
        if number:
            mobile_file.writelines(number)
            mobile_file.writelines('\n')
        rest_file.writelines(rest)

    mobile_file.close()
    rest_file.close()


def person_name(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    name_file = open('name.txt', 'w', encoding='utf-8')
    org_file = open('org.txt', 'w', encoding='utf-8')
    for line in lines:
        space = line.find('-')

        name = line[1:space]
        org = line[space:]
        if name:
            if (len(name) < 6) & (name != '负责人'):
                name_file.writelines(name)
                name_file.writelines('\n')
        org_file.writelines(org)

    org_file.close()
    name_file.close()


if __name__ == '__main__':
    # local_phone('orgs_infos.txt')
    # mobile_phone('rest_info.txt')
    # person_name('rest_name.txt')
    file = open('./crawl/links_crawled.txt', 'r', encoding='utf-8')
    lines = file.readlines()
    file.close()
    lines = list(set(lines))
    with open('urls.txt', 'w', encoding='utf-8') as file:
        for line in lines:
            if len(line) > 4:
                file.writelines(line)
