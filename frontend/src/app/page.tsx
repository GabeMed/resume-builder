"use client";

import UploadForm from "@/components/UploadForm";

const HomePage = () => {
  return (
    <main>
      <div style={{ display: "flex", justifyContent: "center" }}>
        <h1>AI powered Resume Guru</h1>
      </div>
      <UploadForm />
    </main>
  );
};

export default HomePage;
