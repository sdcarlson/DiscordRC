
export const ConvertJson = (roleData, channelData, serverData) => {

    let jsonObj = {
        ...serverData,
        roles: [],
        categories: []
    }

    for (let i = 0; i < roleData.length; i++) {
        let role = {
            name: roleData[i].name,
            id: roleData[i].originalId,
            permissions: Object.keys(roleData[i].permissions).filter(key => roleData[i].permissions[key] === "True")
        }
        jsonObj.roles.push(role)
    }

    const roleIdNameMapping = roleData.reduce((acc, role) => {
        acc[role.id] = role.name;
        return acc;
    }, {})

    let currCategory = {
        "name": null,
        "id": null,
        "permissions": null,
        "text_based_channels": [],
        "voice_based_channels": []
    }
    for (let i = 0; i < channelData.length; i++) {
        if (channelData[i].type !== "category") {
            if (channelData[i].type === "voice") {
                const currChannel = {
                    "name": channelData[i].name,
                    "id": channelData[i].originalId,
                    "channel_type": "VOICE",
                    "permissions": convertPermissions(channelData[i].permissions, roleIdNameMapping)
                }
                currCategory.voice_based_channels.push(currChannel)
            } else if (channelData[i].type === "text") {
                const currChannel = {
                    "name": channelData[i].name,
                    "id": channelData[i].originalId,
                    "channel_type": "TEXT",
                    "permissions": convertPermissions(channelData[i].permissions, roleIdNameMapping)
                }
                currCategory.text_based_channels.push(currChannel)
            }
        } else {
            jsonObj.categories.push(currCategory)
            currCategory = {
                "name": channelData[i].name,
                "id": channelData[i].originalId,
                "permissions": convertPermissions(channelData[i].permissions, roleIdNameMapping),
                "text_based_channels": [],
                "voice_based_channels": []
            }
        }
    }
    jsonObj.categories.push(currCategory)
    return jsonObj
}

const convertPermissions = (permissions, roleIdNameMapping) => {
    let converted =  {}
    let everyone = Object.fromEntries(
        Object.entries(permissions['@everyone']).filter(([key, value]) => value !== 'Inherit')
    )
    for (const key in roleIdNameMapping) {
        if (key !== '@everyone') {
            if (key in permissions) {
                let withoutInherit = Object.fromEntries(
                    Object.entries(permissions[key]).filter(([key, value]) => value !== 'Inherit')
                )
                converted[roleIdNameMapping[key]] = { ...everyone, ...withoutInherit }
            } else {
                converted[roleIdNameMapping[key]] = { ...everyone }
            }
        }
    }
    return converted
}