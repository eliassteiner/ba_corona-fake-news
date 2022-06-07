$files = Get-ChildItem -Path 'C:\Users\mail\Downloads\articles'
$i=0
'"url","date","source","label","header","article","twitter-history"' |  Out-File 'G:\My Drive\BA\0.4\Sources\full.csv' -Encoding UTF8
foreach($file in $files)
{
    echo $i
    $data = Get-Content $file.FullName -Raw -Encoding UTF8 | ConvertFrom-Json
    $data |  ConvertTo-csv | select -Skip 2 | Out-File 'G:\My Drive\BA\0.4\Sources\full.csv' -Encoding UTF8 -Append
    $i++
    
}