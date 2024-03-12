import React, { useEffect, useState } from "react";
import Stack from "@mui/material/Stack";
import Container from "@mui/material/Container";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import FormControl from '@mui/material/FormControl';
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import { useTheme } from "@mui/material/styles";
import { useFormContext } from "../context/FormContext";
import { FromJson } from "../utils/FromJson";
import { useNavigate } from "react-router-dom";

const ServerSelectPage = () => {
  const {
    serverData,
    channelData,
    roleData,
    setServerData,
    setChannelData,
    setRoleData,
  } = useFormContext();

  const [selectedServer, setSelectedServer] = useState("");

  const servers = [
    // replace with function that gets servers from db
    { id: "1", name: "Server 1" },
    { id: "2", name: "Server 2" },
  ];

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

  return (
    <Container
      maxWidth="lg"
      sx={{
        background: "#FFFFFF",
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
              <Button variant="contained">Create Server</Button>
            </Stack>
          </div>
        ) : (
          <></>
        )}
        <FormControl
          fullWidth
          sx={{
            mt: 3,
            mb: 2,
            backgroundColor: "primary.dark",
            color: "text.primary",
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
                borderColor: "transparent",
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
                key={server.id}
                value={server.id}
                sx={{ justifyContent: "center", fontSize: "16px" }}
              >
                {server.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Container>
    </Container>
  );
};

export default ServerSelectPage;
