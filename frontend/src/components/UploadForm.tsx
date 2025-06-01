"use client";

import { Box, Button, Stack, TextField } from "@mui/material";
import React, { useState } from "react";

const UploadForm = () => {
  const [jobTitle, setJobTitle] = useState<string>("");
  const [file, setFile] = useState<File | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log(`Analyze "${file?.name}" for position "${jobTitle}"`);
  };

  return (
    <Box component="form" flexDirection="column">
      <Stack direction="row" justifyContent="center" spacing={4} padding={3}>
        <TextField
          label="Desired position title"
          value={jobTitle}
          onChange={(e) => setJobTitle(e.target.value)}
          required
        ></TextField>
        <Button variant="contained" component="label">
          {file ? file.name : "Upload a PDF/DOCX"}
          <input
            type="file"
            accept=".pdf, .docx"
            hidden
            onChange={(e) => setFile(e.target.files?.[0] || null)}
          ></input>
        </Button>
      </Stack>
      <Stack direction="row" justifyContent="center">
        <Button
          type="submit"
          variant="contained"
          color="primary"
          onSubmit={handleSubmit}
        >
          Upload & Analyze
        </Button>
      </Stack>
    </Box>
  );
};

export default UploadForm;
