import ThemeRegistry from "@/components/ThemeRegistry";

export const metadata = {
  title: "Resume Builder MVP",
  description: "AI-powered resume reviewr",
};

const layout = ({ children }: { children: React.ReactNode }) => {
  return (
    <html lang="en">
      <body>
        <ThemeRegistry>{children}</ThemeRegistry>
      </body>
    </html>
  );
};

export default layout;
