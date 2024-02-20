import CustomTable from "../components/CustomTable";

const RolePage = () => {
    return (
        <CustomTable 
            headings={['Role Name','Display Separately','Allow Mentions','Permission1', 'Permission2']} 
            rownames={['name', 'display_separately', 'allow_mention', 'roleperm1', 'roleperm2']} 
            rowtypes={['text', 'slider', 'slider', 'slider', 'slider']}
            context='role'
        />
    );
}

export default RolePage;