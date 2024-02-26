import { createContext, useState, useEffect, useContext } from "react"

const FormContext = createContext({})

export const FormProvider = ({ children }) => {

    const [roleData, setRoleData] = useState([{
        name: 'temp',
        display_separately: 'False',
        allow_mention: 'False',
        roleperm1: 'True',
        roleperm2: 'True'
      }, {
        name: 'temp2',
        display_separately: 'True',
        allow_mention: 'True',
        roleperm1: 'True',
        roleperm2: 'True'
      }, {
        name: 'temp3',
        display_separately: 'True',
        allow_mention: 'False',
        roleperm1: 'False',
        roleperm2: 'True'
      }, {
        name: 'temp4',
        display_separately: 'True',
        allow_mention: 'True',
        roleperm1: 'True',
        roleperm2: 'False'
    }]) // FIXME: temp replace with []

    return (
        <FormContext.Provider value={{ roleData, setRoleData }}> 
            {children}
        </FormContext.Provider>
    )
}

export const useFormContext = () => {
    return useContext(FormContext)
}

export default FormContext 