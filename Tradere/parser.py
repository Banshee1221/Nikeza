settings_dict = {
    "general": {}
}


def get_settings():
    return settings_dict


with open("vars.conf", "r") as infile:
    current_dict = ""
    for lines in infile:
        lines = lines.strip()
        if lines[0] == "[":
            current_dict = lines[1:-1].lower()
            if current_dict not in settings_dict:
                raise SyntaxError("Incorrect entry in configuration file \"{0}\"".format(lines))
            continue
        tmp = lines.strip().split("=")
        settings_dict[current_dict][tmp[0]] = tmp[1]

if __name__ == "__main__":
    print(settings_dict)
