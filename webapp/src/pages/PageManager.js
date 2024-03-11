import React from 'react'
import { useFormContext } from '../context/FormContext';
import ServerSelectPage from './ServerSelectPage';
import ConfigurationPage from './ConfigurationPage';
import EndPage from './EndPage';

const PageManager = () => {
    const {
        page,
    } = useFormContext()

    const getPage = () => {
        switch(page) {
            case 0:
                return <ServerSelectPage />
            case 1:
                return <ConfigurationPage />
            case 2:
                return <EndPage />
            default:
        }
    }

    return getPage()
    
}

export default PageManager;