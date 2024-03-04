import { createContext, useState, useEffect, useContext } from "react"
import { v4 as uuid } from 'uuid'; // temp


const FormContext = createContext({})

export const FormProvider = ({ children }) => {

    const [channelData, setChannelData] = useState([{
      id: uuid(),
      name: 'temp',
      permissions: {}
    }])

    const [roleData, setRoleData] = useState([{
        id: uuid(),
        name: 'temp',
        permissions: {
          display_separately: 'False',
          roleperm1: 'True',
          roleperm2: 'True'
        }
      }, {
        id: uuid(),
        name: 'temp2',
        permissions: {
          display_separately: 'True',
          allow_mention: 'True',
          roleperm1: 'True',
          roleperm2: 'True'
        }
      }, {
        id: uuid(),
        name: 'temp3',
        permissions: {
          display_separately: 'True',
          allow_mention: 'False',
          roleperm1: 'False',
          roleperm2: 'True'
        }
      }, {
        id: uuid(),
        name: 'temp4',
        permissions: {
          display_separately: 'True',
          allow_mention: 'True',
          roleperm1: 'True',
          roleperm2: 'False'
        }
    }]) // FIXME: temp replace with []

    return (
        <FormContext.Provider value={{ roleData, setRoleData, channelData, setChannelData }}> 
            {children}
        </FormContext.Provider>
    )
}

export const useFormContext = () => {
    return useContext(FormContext)
}

export default FormContext 