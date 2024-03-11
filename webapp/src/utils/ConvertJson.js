
export const ConvertJson = (roleData, channelData, serverData) => {
    console.log(roleData)
    console.log(channelData)
    console.log(serverData)
    const roleIdNameMapping = roleData.reduce((acc, role) => {
        acc[role.id] = role.name;
        return acc;
      }, {});

    let jsonObj = {
        ...serverData,
        roles: [],
        categories: []
    }

    console.log(Object.keys(roleData[i][permissions]))
    for (let i = 0; i < roleData.length; i++) {
        let role = {
            name: roleData[i].name,
            id: roleData[i].originalId,
            permissions: Object.keys(roleData[i][permissions]).filter(key => roleData[i][permissions][key] === "True")
        }
        jsonObj.roles.push(role)
    }

    
    console.log(jsonObj)
    return jsonObj
}