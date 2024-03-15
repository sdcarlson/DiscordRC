
import { v4 as uuid } from 'uuid';

export const FromJson = (setServerData, setChannelData, setRoleData, config) => {
    console.log("Converting from json object...");
    console.log(config);

    setServerData({
        name: config.name,
        id: config.id,
        community: config.community,
    });

    let roles = [];
    let roleIds = {};  // Maps a role name to uuid
    for (const configRole of config.roles) {
        let newRole = {};
        newRole.id = uuid();
        newRole.name = configRole.name;
        newRole.originalId = configRole.id && configRole.id.toString();
        newRole.permissions = {};
        for (const perm of configRole.permissions) {
            newRole.permissions[perm] = 'True';
        }
        roles.push(newRole);
        roleIds[newRole.name] = newRole.id;
    }
    setRoleData(roles);

    let channels = [];
    for (const configCategory of config.categories) {
        if (configCategory.name !== null) {
            let categoryChannel = {};
            categoryChannel.id = uuid();
            categoryChannel.name = configCategory.name;
            categoryChannel.originalId = configCategory.id && configCategory.id.toString();
            categoryChannel.type = 'category';
            let perms = { '@everyone': {} };
            for (const roleName in configCategory.permissions) {
                perms[roleIds[roleName]] = {};
                for (const permName in configCategory.permissions[roleName]) {
                    perms[roleIds[roleName]][permName] =
                        configCategory.permissions[roleName][permName] ? 'True' : 'False';
                }
            }
            categoryChannel.permissions = perms;
            channels.push(categoryChannel);
        }

        for (const configTextChannel of configCategory.text_based_channels) {
            let textChannel = {};
            textChannel.id = uuid();
            textChannel.name = configTextChannel.name;
            textChannel.originalId = configTextChannel.id && configTextChannel.id.toString();
            textChannel.type = configTextChannel.channel_type.toLowerCase();
            let perms = { '@everyone': {} };
            for (const roleName in configTextChannel.permissions) {
                perms[roleIds[roleName]] = {};
                for (const permName in configTextChannel.permissions[roleName]) {
                    perms[roleIds[roleName]][permName] =
                        configTextChannel.permissions[roleName][permName] ? 'True' : 'False';
                }
            }
            textChannel.permissions = perms;
            channels.push(textChannel);
        }

        for (const configVoiceChannel of configCategory.voice_based_channels) {
            let voiceChannel = {};
            voiceChannel.id = uuid();
            voiceChannel.name = configVoiceChannel.name;
            voiceChannel.originalId = configVoiceChannel.id && configVoiceChannel.id.toString();
            voiceChannel.type = configVoiceChannel.channel_type.toLowerCase();
            let perms = { '@everyone': {} };
            for (const roleName in configVoiceChannel.permissions) {
                perms[roleIds[roleName]] = {};
                for (const permName in configVoiceChannel.permissions[roleName]) {
                    perms[roleIds[roleName]][permName] =
                        configVoiceChannel.permissions[roleName][permName] ? 'True' : 'False';
                }
            }
            voiceChannel.permissions = perms;
            channels.push(voiceChannel);
        }
    }
    setChannelData(channels);
}
