Add-Type -AssemblyName System.Drawing
$code = @'
using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.Linq;

public static class ImgConverter {
    public static void Convert(string srcPath, string dstPath, int maxW, int maxH, long quality) {
        using (var img = Image.FromFile(srcPath)) {
            int w = img.Width, h = img.Height;
            double ratio = Math.Min((double)maxW / w, (double)maxH / h);
            if (ratio < 1) { w = (int)(w * ratio); h = (int)(h * ratio); }
            using (var bmp = new Bitmap(w, h)) {
                using (var g = Graphics.FromImage(bmp)) {
                    g.InterpolationMode = System.Drawing.Drawing2D.InterpolationMode.HighQualityBicubic;
                    g.DrawImage(img, 0, 0, w, h);
                }
                var jpegCodec = ImageCodecInfo.GetImageEncoders().FirstOrDefault(c => c.FormatID == ImageFormat.Jpeg.Guid);
                var ep = new EncoderParameters(1);
                ep.Param[0] = new EncoderParameter(Encoder.Quality, quality);
                bmp.Save(dstPath, jpegCodec, ep);
            }
        }
    }
}
'@
Add-Type -TypeDefinition $code -ReferencedAssemblies System.Drawing

$bgDir = "d:\Story game\web-game\assets\backgrounds"
$charDir = "d:\Story game\web-game\assets\characters"
$totalBefore = 0
$totalAfter = 0
$count = 0

Get-ChildItem "$bgDir\*.png" | ForEach-Object {
    $dst = $_.FullName -replace '\.png$', '.jpg'
    [ImgConverter]::Convert($_.FullName, $dst, 1280, 720, 80)
    $before = $_.Length
    $after = (Get-Item $dst).Length
    $totalBefore += $before
    $totalAfter += $after
    $count++
    Write-Output ("BG {0}: {1:N1}MB -> {2:N1}MB" -f $_.Name, ($before/1MB), ($after/1MB))
}

Get-ChildItem "$charDir\*.png" | ForEach-Object {
    $dst = $_.FullName -replace '\.png$', '.jpg'
    [ImgConverter]::Convert($_.FullName, $dst, 1280, 720, 85)
    $before = $_.Length
    $after = (Get-Item $dst).Length
    $totalBefore += $before
    $totalAfter += $after
    $count++
    Write-Output ("CHAR {0}: {1:N1}MB -> {2:N1}MB" -f $_.Name, ($before/1MB), ($after/1MB))
}

Write-Output ""
Write-Output ("Total files: {0}" -f $count)
Write-Output ("Before: {0:N1} MB" -f ($totalBefore/1MB))
Write-Output ("After: {0:N1} MB" -f ($totalAfter/1MB))
Write-Output ("Reduction: {0:N1}%" -f ((1 - $totalAfter/$totalBefore) * 100))
