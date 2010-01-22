require 'RMagick'
require 'rubygems'
require 'json'

data = []

image_d = Dir.open('../image')



image_d.each do |f|
  match = /(\d)+/.match(f)
  if match
    num = match[0].to_s
    data << ["../image/" + f, ] 
  end
end

data.sort!

data.each_with_index do |d, i|
  img = Magick::ImageList.new(d[0])
  img.resize_to_fit(900,900)
  img.write("../archive/image/small/fractal#{i.to_s.rjust(5,'0')}.jpg")
  `cp ./#{d[0]} ../archive/image/full/fractal#{i.to_s.rjust(5,'0')}.png`

  puts "done img " + i.to_s

end

