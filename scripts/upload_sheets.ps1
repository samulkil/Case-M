# Upload resultados.csv para Google Sheets via API REST pura (zero dependencias externas)
# Compativel com Windows PowerShell 5.1 / .NET Framework 4.x

param(
    [string]$CredentialsPath = "$PSScriptRoot\..\electric-block-499518-u6-13b4833e0c5c.json",
    [string]$ResultsPath     = "$PSScriptRoot\..\resultados.csv",
    [string]$SpreadsheetId   = "11n95hFQzc-ax-iLg6tuLK7R4-48DNH9zAth1S6dN7XI",
    [string]$SheetName       = "P" + [char]0xe1 + "gina1"
)

$ErrorActionPreference = "Stop"

function ConvertTo-Base64Url([byte[]]$bytes) {
    [Convert]::ToBase64String($bytes).TrimEnd('=').Replace('+','-').Replace('/','_')
}

function Import-RsaFromPkcs8Pem([string]$pem) {
    $b64 = $pem -replace '-----BEGIN PRIVATE KEY-----','' -replace '-----END PRIVATE KEY-----','' -replace '\s',''
    [byte[]]$der = [Convert]::FromBase64String($b64)
    $pos = [ref]0
    function Read-Len([byte[]]$d,[ref]$p){$b=$d[$p.Value];$p.Value++;if($b -lt 0x80){return [int]$b};$n=$b -band 0x7F;$v=0;for($i=0;$i -lt $n;$i++){$v=($v -shl 8) -bor $d[$p.Value];$p.Value++};return $v}
    function Skip-Tag([byte[]]$d,[ref]$p,[byte]$t){if($d[$p.Value] -ne $t){throw "DER tag"};$p.Value++}
    function Read-Int([byte[]]$d,[ref]$p){Skip-Tag $d $p 0x02;$l=Read-Len $d $p;$b=$d[$p.Value..($p.Value+$l-1)];$p.Value+=$l;if($b[0] -eq 0x00 -and $b.Length -gt 1){$b=$b[1..($b.Length-1)]};return [byte[]]$b}
    Skip-Tag $der $pos 0x30; Read-Len $der $pos | Out-Null
    Skip-Tag $der $pos 0x02; $vl=Read-Len $der $pos; $pos.Value+=$vl
    Skip-Tag $der $pos 0x30; $al=Read-Len $der $pos; $pos.Value+=$al
    Skip-Tag $der $pos 0x04; Read-Len $der $pos | Out-Null
    Skip-Tag $der $pos 0x30; Read-Len $der $pos | Out-Null
    Skip-Tag $der $pos 0x02; $rv=Read-Len $der $pos; $pos.Value+=$rv
    $rp=New-Object System.Security.Cryptography.RSAParameters
    $rp.Modulus=Read-Int $der $pos; $rp.Exponent=Read-Int $der $pos; $rp.D=Read-Int $der $pos
    $rp.P=Read-Int $der $pos; $rp.Q=Read-Int $der $pos; $rp.DP=Read-Int $der $pos
    $rp.DQ=Read-Int $der $pos; $rp.InverseQ=Read-Int $der $pos
    $rsa=New-Object System.Security.Cryptography.RSACryptoServiceProvider
    $rsa.ImportParameters($rp); return $rsa
}

# ── 1. Credenciais ─────────────────────────────────────────────────────────────
$creds = Get-Content $CredentialsPath -Raw | ConvertFrom-Json

# ── 2. JWT + Access Token ──────────────────────────────────────────────────────
$now=[DateTimeOffset]::UtcNow.ToUnixTimeSeconds(); $exp=$now+3600
$hdr=ConvertTo-Base64Url([Text.Encoding]::UTF8.GetBytes('{"alg":"RS256","typ":"JWT"}'))
$clmJson='{"iss":"'+$creds.client_email+'","scope":"https://www.googleapis.com/auth/spreadsheets","aud":"https://oauth2.googleapis.com/token","iat":'+$now+',"exp":'+$exp+'}'
$clm=ConvertTo-Base64Url([Text.Encoding]::UTF8.GetBytes($clmJson))
$sigInput="$hdr.$clm"
$rsa=Import-RsaFromPkcs8Pem $creds.private_key
$sigB=$rsa.SignData([Text.Encoding]::UTF8.GetBytes($sigInput),[Security.Cryptography.SHA256]::Create())
$jwt="$sigInput.$(ConvertTo-Base64Url $sigB)"

$tok=Invoke-RestMethod -Method Post -Uri "https://oauth2.googleapis.com/token" `
    -ContentType "application/x-www-form-urlencoded" `
    -Body "grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Ajwt-bearer&assertion=$jwt"
$auth=@{Authorization="Bearer $($tok.access_token)"}

# ── 3. Ler CSV com parser robusto (campos com virgulas nao precisam de aspas) ──
# Schema fixo: nome_teste,descricao,variante_vencedora,decisao,data_analise (5 colunas)
# Estrategia: split nas primeiras 4 virgulas; tudo que sobrar vai para decisao
function Parse-CsvLine([string]$line) {
    # Remove aspas duplas que envolvem o campo inteiro, se houver
    $result = @()
    $remaining = $line
    for ($col = 0; $col -lt 4; $col++) {
        if ($remaining.StartsWith('"')) {
            # Campo entre aspas: encontrar fechamento
            $end = $remaining.IndexOf('"', 1)
            while ($end -lt $remaining.Length - 1 -and $remaining[$end+1] -eq '"') { $end = $remaining.IndexOf('"', $end+2) }
            $result += $remaining.Substring(1, $end-1) -replace '""','"'
            $remaining = if ($end+2 -lt $remaining.Length) { $remaining.Substring($end+2) } else { '' }
        } else {
            $idx = $remaining.IndexOf(',')
            if ($idx -lt 0) { $result += $remaining; $remaining = ''; break }
            $result += $remaining.Substring(0, $idx)
            $remaining = $remaining.Substring($idx+1)
        }
    }
    $result += $remaining.Trim('"')
    return $result
}

$rawLines = Get-Content $ResultsPath -Encoding UTF8
if ($rawLines.Count -le 1) { Write-Host "resultados.csv vazio - nada a enviar."; exit 0 }
$dataLines = $rawLines | Select-Object -Skip 1 | Where-Object { $_.Trim() -ne '' }

# ── 4. Montar JSON manualmente (garante array de arrays) ──────────────────────
$esc = { param($s) ($s + '') -replace '\\','\\' -replace '"','\"' }
$lines = @()
$lines += '["nome_teste","descricao","variante_vencedora","decisao","data_analise"]'
foreach ($dl in $dataLines) {
    $f = Parse-CsvLine $dl
    while ($f.Count -lt 5) { $f += '' }
    $lines += '["'+(&$esc $f[0])+'","'+(&$esc $f[1])+'","'+(&$esc $f[2])+'","'+(&$esc $f[3])+'","'+(&$esc $f[4])+'"]'
}
$body = '{"range":"'+$SheetName+'!A1","majorDimension":"ROWS","values":['+($lines -join ',')+']}'

# ── 5. Limpar e gravar ─────────────────────────────────────────────────────────
$encClear  = [Uri]::EscapeDataString($SheetName + "!A:Z")
$encAppend = [Uri]::EscapeDataString($SheetName + "!A1")

try {
    Invoke-RestMethod -Method Post `
        -Uri "https://sheets.googleapis.com/v4/spreadsheets/$SpreadsheetId/values/${encClear}:clear" `
        -Headers $auth -ContentType "application/json" -Body "{}" | Out-Null
} catch { }

$res = Invoke-RestMethod -Method Post `
    -Uri "https://sheets.googleapis.com/v4/spreadsheets/$SpreadsheetId/values/${encAppend}:append?valueInputOption=RAW&insertDataOption=OVERWRITE" `
    -Headers $auth -ContentType "application/json; charset=utf-8" `
    -Body ([Text.Encoding]::UTF8.GetBytes($body))

Write-Host "Google Sheets atualizado: $($res.updates.updatedRows) linha(s) gravadas na aba '$SheetName'."
