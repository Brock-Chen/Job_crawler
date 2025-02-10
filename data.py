def condition(data) :
    major, skill, specialty = "", "", ""
    for s in data["major"] :
        major+=(s+", ")
    for obj in data["skill"] :
        skill+=(obj["description"]+", ")
    for obj in data["specialty"] :
        specialty+=(obj["description"]+", ")
    return f"工作經歷: {data['workExp']}\n學歷要求: {data['edu']}\n科系要求: {major}\n擅長工具: {skill}\n工作技能: {specialty}\n其他條件: {data['other']}"