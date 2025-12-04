#define ConfigFile "config.ini"
#define MyAppName "{#ReadIniValue(ConfigFile, 'AppInfo', 'AppName')}"
#define MyAppVersion "{#ReadIniValue(ConfigFile, 'AppInfo', 'AppVersion')}"
#define MyAppPublisher "{#ReadIniValue(ConfigFile, 'AppInfo', 'AppPublisher')}"
#define MyAppPublisherURL "{#ReadIniValue(ConfigFile, 'AppInfo', 'AppPublisherURL')}"
#define MyAppExeName "{#ReadIniValue(ConfigFile, 'AppInfo', 'AppExeName')}"
#define DefaultEncoding "{#ReadIniValue(ConfigFile, 'Encodings', 'DefaultEncoding')}"
#define PreferredEncoding "{#ReadIniValue(ConfigFile, 'Encodings', 'PreferredEncoding')}"
#define PythonExecutable "{#ReadIniValue(ConfigFile, 'Python', 'PythonExecutable')}"
#define CharsetNormalizer "{#ReadIniValue(ConfigFile, 'Python', 'CharsetNormalizer')}"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppPublisherURL}
AppSupportURL={#MyAppPublisherURL}
AppUpdatesURL={#MyAppPublisherURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=Output
OutputBaseFilename=ConversorCodificacion_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
DisableProgramGroupPage=no
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Files]
Source: "conversor.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#CharsetNormalizer}"; DestDir: "{tmp}"; Flags: external

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Run]
Filename: "{#PythonExecutable}"; Parameters: """{app}\{#MyAppExeName}"""; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent runascurrentuser

[Code]
function ReadIniValue(const IniFile, Section, Key: string): string;
var
  Ini: TIniFile;
begin
  Result := '';
  Ini := TIniFile.Create(IniFile);
  try
    Result := Ini.ReadString(Section, Key, '');
  finally
    Ini.Free;
  end;
end;

function InitializeSetup(): Boolean;
begin
  if not RegKeyExists(HKLM, 'SOFTWARE\Python\PythonCore') and
     not RegKeyExists(HKLM64, 'SOFTWARE\Python\PythonCore') then
  begin
    MsgBox('Python no está instalado. Por favor, instala Python 3.7 o superior desde python.org', mbError, MB_OK);
    Result := False;
  end
  else
    Result := True;
end;
