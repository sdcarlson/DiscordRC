import { createContext, useState, useContext } from "react"
import { v4 as uuid } from 'uuid'; // temp


const FormContext = createContext({})

export const FormProvider = ({ children }) => {

    const [page, setPage] = useState(0)

    const [serverData, setServerData] = useState({
      name: '',
      id: null,
      community: false
    })

    const [channelData, setChannelData] = useState([{
      id: uuid(),
      name: 'temp',
      type: 'voice',
      originalId: "128",
      permissions: {
        '@everyone': {
          "mention_everyone": 'False',
          "use_external_emojis": 'False',
          "use_external_stickers": 'False'
        }
      }
    }, {
      id: uuid(),
      name: 'temp2',
      originalId: "127",
      type: 'text',
      permissions: {
        '@everyone': {

        }
      }
    }])

    const [roleData, setRoleData] = useState([{
        id: uuid(),
        name: 'temp',
        originalId: "126",
        permissions: {
          display_separately: 'False',
          roleperm1: 'True',
          roleperm2: 'True'
        }
      }, {
        id: uuid(),
        name: 'temp2',
        originalId: "125",
        permissions: {
          display_separately: 'True',
          allow_mention: 'True',
          roleperm1: 'True',
          roleperm2: 'True'
        }
      }, {
        id: uuid(),
        name: 'temp3',
        originalId: "124",
        permissions: {
          display_separately: 'True',
          allow_mention: 'False',
          roleperm1: 'False',
          roleperm2: 'True'
        }
      }, {
        id: uuid(),
        name: 'temp4',
        originalId: "123",
        permissions: {
          display_separately: 'True',
          allow_mention: 'True',
          roleperm1: 'True',
          roleperm2: 'False'
        }
    }]) // FIXME: temp replace with []

    return (
        <FormContext.Provider value={{ page, setPage, roleData, setRoleData, channelData, setChannelData, serverData, setServerData }}> 
            {children}
        </FormContext.Provider>
    )
}

export const useFormContext = () => {
    return useContext(FormContext)
}

export default FormContext 