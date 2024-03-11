import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Button,
  Container,
  MenuItem,
  FormControl,
  Select,
} from "@mui/material";

const HomePage = () => {
  const [selectedServer, setSelectedServer] = useState("");
  //const navigate = useNavigate();

  const servers = [
    { id: "1", name: "Server 1" },
    { id: "2", name: "Server 2" },
  ];

  const handleServerChange = (event) => {
    setSelectedServer(event.target.value);
  };

  return (
    <Container
      component="main"
      maxWidth="xs"
      sx={{
        mt: 8,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
      }}
    >
      <Button
        variant="contained"
        sx={{
          mt: 3,
          mb: 2,
          backgroundColor: "primary.dark",
          color: "text.primary",
          width: "100%",
          fontSize: "16px",
        }}
      >
        Create Server from Scratch
      </Button>
      <Button
        variant="contained"
        sx={{
          mt: 3,
          mb: 2,
          backgroundColor: "primary.dark",
          color: "text.primary",
          width: "100%",
          fontSize: "16px",
        }}
      >
        Upload JSON
      </Button>
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
  );
};

export default HomePage;
