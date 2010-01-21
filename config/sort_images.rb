require 'RMagick'

files = []

d = Dir.open('./')

d.each do |f|
  files << f if f =~ /.png/
end

files.each_with_index do |f, i|
  img = Magick::ImageList.new(f)
  img.resize_to_fit(900,900)
  img.write("small/fractal#{i}.jpg")
  `cp ./#{f} full/fractal#{i}.png`
end
