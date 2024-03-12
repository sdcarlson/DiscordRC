import React, { useEffect, useState } from "react";
import Stack from "@mui/material/Stack";
import Container from "@mui/material/Container";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import { useTheme } from "@mui/material/styles";
import { useFormContext } from "../context/FormContext";
import { FromJson } from "../utils/FromJson";
import { useNavigate } from "react-router-dom";
import CircularProgress from "@mui/material/CircularProgress";
import { Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Link } from "@mui/material";

const ServerSelectPage = () => {
  const {
    serverData,
    channelData,
    roleData,
    setServerData,
    setChannelData,
    setRoleData,
  } = useFormContext();

  const [servers, setServers] = useState([]);
  const [selectedServer, setSelectedServer] = useState("");
  const [isLoading, setIsLoading] = useState(false)
  const [createServerDialog, setCreateServerDialog] = useState(false);
  const [serverLink, setServerLink] = useState("");

  const handleServerChange = (event) => {
    setSelectedServer(event.target.value);
  };

  const navigate = useNavigate();

  const theme = useTheme();

  const [file, setFile] = useState();
  function handleUpload(event) {
    setFile(event.target.files[0]);
  }

  const [config, setConfig] = useState();

  useEffect(() => {
    let reader = new FileReader();
    reader.addEventListener(
      "load",
      () => {
        const config = JSON.parse(reader.result);
        setConfig(config);
      },
      false
    );
    if (file) {
      reader.readAsText(file);
    }
  }, [file]);

  useEffect(() => {
    fetchServers();
  }, []);

  const fetchServers = async () => {
    const accessToken = localStorage.getItem("access_token");
    const authStr = "Bearer " + accessToken;
    try {
      const response = await fetch("http://localhost:8000/users/me", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: authStr,
        },
      });
      if (!response.ok) {
        throw new Error("Network error");
      }
      const data = await response.json();
      console.log(data)
      setServers(data.servers || []);
    } catch (error) {
      console.error(
        "There was a problem with the server fetch operation:",
        error
      );
    }
  };

  const handleCreateServer = async() => {
    setIsLoading(true);
    const response = await fetch("http://localhost:8000/bot/create", {
        method: "POST",
        headers: new Headers({
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem("access_token")
        }),
        body: JSON.stringify(config),
    });

    if (response.ok) {
        console.log("Server creation successful");
        const json = await response.json();
        setCreateServerDialog(true);
        setServerLink(json.invite_link);
    } else {
        console.error("Server creation failed");
    }
    setIsLoading(false);
  }

const handleGetServerConfig = async() => {
    setIsLoading(true);
    const response = await fetch("http://localhost:8000/config/export?server_name="+selectedServer, {
        method: "GET",
        headers: new Headers({
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem("access_token")
        }),
    });

    if (response.ok) {
        console.log("Server loaded successfully");
        const json = await response.json();
        console.log(json);
        FromJson(setServerData, setChannelData, setRoleData, json);
        navigate("/config");
    } else {
        console.error("Server load failed");
    }
    setIsLoading(false);
  }

  return (
    <Container
      maxWidth="lg"
      sx={{
        marginTop: theme.spacing(10),
        marginBottom: theme.spacing(5),
      }}
    >
      <Container sx={{ padding: 5 }}>
        <Stack spacing={3} alignItems="center" justifyContent="center">
          <Typography variant="h2">DiscordRC Server Configuration</Typography>
          <TextField
            label="Server Name"
            defaultValue={serverData.name}
            helperText="Enter new server name and hit configure, or upload from JSON"
            variant="standard"
            onChange={(event) => {
              let tempServerData = { ...serverData };
              tempServerData.name = event.target.value;
              setServerData(tempServerData);
            }}
          />
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
            onClick={() => {
              setChannelData([]);
              setRoleData([]);
              navigate("/config");
            }}
          >
            Configure New
          </Button>
          <Button variant="contained" component="label">
            Upload Json
            <input type="file" hidden onChange={handleUpload} />
          </Button>
        </Stack>
        {file ? (
          <div>
            <Stack
              sx={{ m: 2 }}
              spacing={5}
              direction="row"
              alignItems="center"
              justifyContent="center"
            >
              <Typography variant="p">Uploaded file: {file.name}</Typography>
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
                onClick={() => {
                  FromJson(setServerData, setChannelData, setRoleData, config);
                  navigate("/config");
                }}
              >
                Edit
              </Button>
              <Button variant="contained" onClick={handleCreateServer}>Create Server</Button>
            </Stack>
          </div>
        ) : (
          <></>
        )}
        <Stack alignItems="center" justifyContent="center">
            <FormControl
            sx={{
                mt: 3,
                mb: 2,
                // backgroundColor: "primary.dark",
                // color: "text.primary",
                minWidth: 500,
                textAlign: "center",
            }}
            >
            <Select
                value={selectedServer}
                onChange={handleServerChange}
                displayEmpty
                inputProps={{ "aria-label": "Without label" }}
                sx={{
                textAlign: "center",
                "& .MuiSelect-select": {
                    textAlignLast: "center",
                    fontSize: "16px",
                },
                "& .MuiOutlinedInput-notchedOutline": {
                    // borderColor: "transparent",
                },
                fontSize: "16px",
                }}
            >
                <MenuItem
                value=""
                disabled
                sx={{ justifyContent: "center", fontSize: "16px" }}
                >
                EDIT SAVED SERVERS
                </MenuItem>
                {servers.map((server) => (
                <MenuItem
                    key={server}
                    value={server}
                    sx={{ justifyContent: "center", fontSize: "16px" }}
                >
                    {server}
                </MenuItem>
                ))}
            </Select>
            </FormControl>
        </Stack>
        <Stack
          sx={{ m: 2 }}
          spacing={5}
          direction="row"
          alignItems="center"
          justifyContent="center"
        >
          {selectedServer !== "" && 
            <Button variant="contained" onClick={handleGetServerConfig}>
                Load Selected Server</Button>
          }
          <Button
            variant="contained"
            onClick={() => {
              localStorage.removeItem("access_token");
              navigate("/");
            }}
          >
            Log Out
          </Button>
        </Stack>
        <Stack
          alignItems="center"
          justifyContent="center"
        >
            {isLoading && <Typography variant='h4'>Currently Loading</Typography>}
            {isLoading && <CircularProgress />}
        </Stack>
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
      </Container>
    </Container>
  );
};

export default ServerSelectPage;
