import requests
from xml.etree import ElementTree as et

User_Input = (
    input("Please enter your main nation for the User-Agent: ")
    .lower()
    .replace(" ", "_")
)
headers = {
    "User-Agent": f"Project Solar requesting region and nation information, devved by nation=Ghazi-Rahman Ammar ibn Rigel Al-Asteorra, in use by {User_Input}"
}

region = input("Please enter target region: ")
resident_nations = requests.get(
    f"https://www.nationstates.net/cgi-bin/api.cgi?region={region.lower().replace(' ','_')}&q=nations",
    headers=headers,
)
delegate_name = requests.get(
    f"https://www.nationstates.net/cgi-bin/api.cgi?region={region.lower().replace(' ','_')}&q=delegate",
    headers=headers,
)

resident_nations_root = et.fromstring(resident_nations.content)
nations = resident_nations_root.find("NATIONS").text.split(":")

delegate_name_root = et.fromstring(delegate_name.content)
Delegate = delegate_name_root.find("DELEGATE").text
residents = [nation for nation in nations if nation != Delegate]

delegate_endos = requests.get(
    f"https://www.nationstates.net/cgi-bin/api.cgi?nation={Delegate}&q=endorsements",
    headers=headers,
)
delegate_endos_root = et.fromstring(delegate_endos.content)
endorsements = delegate_endos_root.find("ENDORSEMENTS").text.split(",")
endorsers = [endorsement for endorsement in endorsements]
non_endorsing = [nation for nation in residents if nation not in endorsements]

print(f"The following nations are not endorsing {Delegate}: {non_endorsing}")