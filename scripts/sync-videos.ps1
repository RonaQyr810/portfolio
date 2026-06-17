# 将桌面「作品集」视频同步到 assets/videos/，供 GitHub Pages 在线播放
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$src = Join-Path (Split-Path $root -Parent) '作品集'
$dst = Join-Path $root 'assets\videos'

$map = @{
    'web-dev' = @{
        'flask-house.mp4'     = '..\学校文档\2220048-秦艺榕\03-课程项目\Flask功能演示.mp4'
        'health-pathway.mp4'  = '01-视频动画\01-从主目录\02-医疗与医生项目\录屏软件医疗网站设置.mp4'
        'modao-web.mp4'       = '..\学校文档\2220048-秦艺榕\03-代码项目\文人四友-网站设计\录屏文件.mp4'
    }
    'xishixiaozhan' = @{
        'user-demo.mp4'  = '..\毕设项目\项目-惜食小站-毕业设计\2220048 秦艺榕 作品展示视频（用户端）.mp4'
        'admin-demo.mp4' = '..\毕设项目\项目-惜食小站-毕业设计\2220048 秦艺榕 作品展示视频（管理端）.mp4'
    }
    'peking-opera' = @{
        'final.mp4'        = '梨园之韵\梨园之韵 最终成品.mp4'
    }
    'campus-media' = @{
        'shizhu.mp4'       = '实训文件\拾筑.mp4'
        'script-video.mp4' = '实训文件\2220048 秦艺榕 剧本视频.mp4'
        'ui-defense.mp4'   = 'UI设计\录屏文件.mp4'
    }
    'ae-effects' = @{
        'mg-intro.mp4'    = '2220048 秦艺榕.mp4'
        'composite-2.mp4' = '2220048 秦艺榕_1.mp4'
    }
    'c4d' = @{
        'ferris-wheel.mp4'   = 'c4d动画合集\摩天轮.mp4'
        'water-roll.mp4'     = 'c4d动画合集\2220048 秦艺榕 滚动的水滴.mp4'
        'swimming-fish.mp4'  = 'c4d动画合集\2220048 秦艺榕 游动的鱼.mp4'
        'pendulum.mp4'       = 'c4d动画合集\2220048 秦艺榕 钟摆.mp4'
        'clock.mp4'          = 'c4d动画合集\2220048 秦艺榕时钟.mp4'
        'cut-sausage.mp4'    = 'c4d动画合集\220048 秦艺榕 切红肠.mp4'
        'variable-speed.mp4' = 'c4d动画合集\2220048 秦艺榕 变速.mp4'
        'path-motion.mp4'    = 'c4d动画合集\2220048 秦艺榕 路径动画.mp4'
        'ball-morph.mp4'     = 'c4d动画合集\2220048 秦艺榕 小球变形.mp4'
        'water-drop.mp4'     = 'c4d动画合集\2220048 秦艺榕 水滴滴落.mp4'
        'growth.mp4'         = 'c4d动画合集\2220048 秦艺榕 生长动画.mp4'
        'parabola.mp4'       = 'c4d动画合集\220048 秦艺榕  小球抛物线.mp4'
        'skeleton.mp4'       = 'c4d动画合集\骨骼.mp4'
        'get-off.mp4'        = 'c4d动画合集\xiache.mp4'
    }
}

function Copy-Video($category, $name, $relative) {
    $outDir = Join-Path $dst $category
    New-Item -ItemType Directory -Force -Path $outDir | Out-Null
    $out = Join-Path $outDir $name
    if ($relative.StartsWith('..\')) {
        $in = Join-Path (Split-Path $root -Parent) ($relative.Substring(3))
    } else {
        $in = Join-Path $src $relative
    }
    if (-not (Test-Path -LiteralPath $in)) {
        Write-Warning "跳过（源文件不存在）: $in"
        return
    }
    Copy-Item -LiteralPath $in -Destination $out -Force
    $mb = [math]::Round((Get-Item -LiteralPath $out).Length / 1MB, 1)
    Write-Host "OK $category/$name ($mb MB)"
}

foreach ($cat in $map.Keys) {
    foreach ($entry in $map[$cat].GetEnumerator()) {
        Copy-Video $cat $entry.Key $entry.Value
    }
}

Write-Host "`n完成。接下来在项目根目录执行："
Write-Host "  git lfs install"
Write-Host "  git add .gitattributes assets/videos scripts/sync-videos.ps1"
Write-Host "  git commit -m `"Add portfolio videos via Git LFS`""
Write-Host "  git push origin main"
Write-Host "  git lfs push origin main --all"
