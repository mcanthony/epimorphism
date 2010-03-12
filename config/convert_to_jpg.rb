require 'rubygems'
require 'RMagick'

image_d = Dir.open('./')

image_d.each do |f|
  img = Magick::ImageList.new(f)
  img.write(f.gsub("png","jpg"))
end
  
