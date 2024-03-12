import React, { useState } from "react";
import Stack from "@mui/material/Stack";
import Container from "@mui/material/Container";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import { useTheme } from "@mui/material/styles";
import { useFormContext } from "../context/FormContext";
import { ConvertJson } from "../utils/ConvertJson";
import { useNavigate } from "react-router-dom";
import CircularProgress from "@mui/material/CircularProgress";
import { Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Link } from "@mui/material";

const EndPage = () => {
  const { roleData, channelData, serverData } = useFormContext();

  const [isLoading, setIsLoading] = useState(false);
  const [createServerDialog, setCreateServerDialog] = useState(false);
  const [saveConfigDialog, setSaveConfigDialog] = useState(false);
  const [serverLink, setServerLink] = useState("");

  const theme = useTheme();
  const navigate = useNavigate();

  const handleDownload = () => {
    const myObject = ConvertJson(roleData, channelData, serverData);
    const jsonString = JSON.stringify(myObject, null, 2);
    const blob = new Blob([jsonString], { type: 'application/json' });
    const blobUrl = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = blobUrl;
    link.download = 'config.json';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(blobUrl);
  };

  const handleCreateServer = async() => {
    setIsLoading(true);
    const response = await fetch("http://localhost:8000/bot/create", {
        method: "POST",
        headers: new Headers({
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem("access_token")
        }),
        body: JSON.stringify(ConvertJson(roleData, channelData, serverData)),
    });

    if (response.ok) {
        console.log("Server creation successful");
        const json = await response.json();
        setCreateServerDialog(true);
        setServerLink(json.invite_link);
        console.log(json);
    } else {
        console.error("Server creation failed");
    }
    setIsLoading(false);
  }

  const handleSaveConfig = async() => {
    setIsLoading(true);
    const response = await fetch("http://localhost:8000/config/import", {
        method: "POST",
        headers: new Headers({
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem("access_token")
        }),
        body: JSON.stringify(ConvertJson(roleData, channelData, serverData)),
    });
    if (response.ok) {
        console.log("Config import successful");
        setSaveConfigDialog(true);
    } else {
        console.error("Config import failed");
    }
    setIsLoading(false);
  }

  return (
    <>
    <Typography
        component="h1"
        variant="h1"
        sx={{ mb: 4, textAlign: "center", fontFamily: 'Fredericka the Great' }}
    >
        DiscordRC
    </Typography>
    <Container
      maxWidth="lg"
      sx={{
        background: "#FFFFFF",
        marginTop: theme.spacing(10),
        marginBottom: theme.spacing(5),
      }}
    >
      <Dialog
        open={createServerDialog}
        onClose={() => setCreateServerDialog(false)}
      >
        <DialogTitle>
          {"Server Created Successfully"}
        </DialogTitle>
        <DialogContent>
          <DialogContentText>
            Join your server <Link href={serverLink} target="_blank" rel="noopener noreferrer">here</Link>
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCreateServerDialog(false)}>Close</Button>
        </DialogActions>
      </Dialog>

      <Dialog
        open={saveConfigDialog}
        onClose={() => setSaveConfigDialog(false)}
      >
        <DialogTitle>
          {"Configuration Saved Successfully"}
        </DialogTitle>
        <DialogContent>
          <DialogContentText>
            Your configuration has been saved successfully
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => navigate("/home")}>Return to Home</Button>
          <Button onClick={() => setSaveConfigDialog(false)}>Close</Button>
        </DialogActions>
      </Dialog>

      <Container sx={{ padding: 5 }}>
        <Stack spacing={10} alignItems="center" justifyContent="center">
          <Typography variant="h2">
            Server "{serverData.name}" Configuration Completed
          </Typography>
          <Box>
            <Stack alignItems="center" justifyContent="center">
                <Typography variant="h5">
                    Select an option below:
                </Typography>
            </Stack>
            <Stack
                sx={{ m: 2 }}
                spacing={5}
                direction="row"
                alignItems="center"
                justifyContent="center"
                >
                <Button
                    variant="contained"
                    onClick={handleDownload}
                    sx = {{
                        maxWidth: "200px",
                        minWidth: "200px",
                    }}
                >
                    Download JSON
                </Button>
                <Button
                    variant="contained"
                    onClick={handleCreateServer}
                    sx = {{
                        maxWidth: "200px",
                        minWidth: "200px",
                    }}
                >
                    Create Server
                </Button>
                <Button
                    variant="contained"
                    onClick={handleSaveConfig}
                    sx = {{
                        maxWidth: "200px",
                        minWidth: "200px",
                    }}
                >
                    Save Config
                </Button>
                </Stack>
            </Box>
            <Button
                variant="contained"
                onClick={() => {
                navigate("/config");
                }}
            >
                Return to Configuration
            </Button>
            <Box>
                {isLoading && <CircularProgress />}
            </Box>
        </Stack>
        

      </Container>
    </Container>
    </>
  );
};

export default EndPage;
