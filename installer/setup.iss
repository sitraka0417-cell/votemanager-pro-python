[Setup]
AppName=VoteManager Pro
AppVersion=1.0
AppPublisher=VoteManager Pro
DefaultDirName={autopf}\VoteManagerPro
DefaultGroupName=VoteManager Pro
OutputDir=installer_output
OutputBaseFilename=VoteManagerPro-Setup
Compression=lzma
SolidCompression=yes
DisableProgramGroupPage=yes
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "french"; MessagesFile: "compiler:Languages\French.isl"

[Files]
Source: "dist\VoteManagerPro\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\VoteManager Pro"; Filename: "{app}\VoteManagerPro.exe"
Name: "{group}\Desinstaller VoteManager Pro"; Filename: "{uninstallexe}"
Name: "{commondesktop}\VoteManager Pro"; Filename: "{app}\VoteManagerPro.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Creer un raccourci sur le Bureau"; GroupDescription: "Raccourcis :"

[Run]
Filename: "{app}\VoteManagerPro.exe"; Description: "Lancer VoteManager Pro"; Flags: nowait postinstall skipifsilent
