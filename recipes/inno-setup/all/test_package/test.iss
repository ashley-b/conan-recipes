#define MyAppName "Test App"

[Setup]
AppName={#MyAppName}
AppVersion=0.1
DefaultDirName={autopf}\{#MyAppName}

[Files]
Source: "test.iss"; DestDir: "{app}"