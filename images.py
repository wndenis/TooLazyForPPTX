from google_images_download import google_images_download

response = google_images_download.googleimagesdownload()
absolute_image_paths = response.download({"limit": 1, "keywords": "пёс",
                                          "time": "past-24-hours", "print_urls": True})
#print(absolute_image_paths)
exit()
# print(random.choice(absolute_image_paths))
