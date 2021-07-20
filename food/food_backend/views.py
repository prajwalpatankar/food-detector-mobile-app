from .serializers import imageSerializer
from .models import MyImage
from rest_framework import viewsets
import requests
from django.shortcuts import render
from django.http import HttpResponse

import torch 
import torchvision.transforms as T
import torchvision.models as models
from torchvision.utils import make_grid
from PIL import Image

class ImageCreateAPIView(viewsets.ModelViewSet):
	serializer_class = imageSerializer
	queryset = MyImage.objects.all()

def model_call(request):
	req_id = request.GET.get('id')
	img_obj = MyImage.objects.get(id=req_id)
	django_img = img_obj.model_pic
	img = Image.open(django_img)

	model_path = "food_backend/mod.pth"	
	device = 'cpu'
	classes = ['apple_pie','baby_back_ribs','baklava','beef_carpaccio','beef_tartare','beet_salad','beignets','bibimbap','bread_pudding','breakfast_burrito','bruschetta','caesar_salad','cannoli','caprese_salad','carrot_cake','ceviche','cheese_plate','cheesecake','chicken_curry','chicken_quesadilla','chicken_wings','chocolate_cake','chocolate_mousse','churros','clam_chowder','club_sandwich','crab_cakes','creme_brulee','croque_madame','cup_cakes','deviled_eggs','donuts','dumplings','edamame','eggs_benedict','escargots','falafel','filet_mignon','fish_and_chips','foie_gras','french_fries','french_onion_soup','french_toast','fried_calamari','fried_rice','frozen_yogurt','garlic_bread','gnocchi','greek_salad','grilled_cheese_sandwich','grilled_salmon','guacamole','gyoza','hamburger','hot_and_sour_soup','hot_dog','huevos_rancheros','hummus','ice_cream','lasagna','lobster_bisque','lobster_roll_sandwich','macaroni_and_cheese','macarons','miso_soup','mussels','nachos','omelette','onion_rings','oysters','pad_thai','paella','pancakes','panna_cotta','peking_duck','pho','pizza','pork_chop','poutine','prime_rib','pulled_pork_sandwich','ramen','ravioli','red_velvet_cake','risotto','samosa','sashimi','scallops','seaweed_salad','shrimp_and_grits','spaghetti_bolognese','spaghetti_carbonara','spring_rolls','steak','strawberry_shortcake','sushi','tacos','takoyaki','tiramisu','tuna_tartare','waffles']


	model = torch.load(model_path, map_location=torch.device(device) )
	for parameter in model.parameters():
		parameter.requires_grad = False

	model.eval()
	# print(model)
		
	test_transforms = T.Compose([
		T.Resize(256),
		T.ToTensor()
	])

	# img = Image.open(image_path)
	image_tensor = test_transforms(img).float()
	image_tensor = image_tensor.unsqueeze_(0)
	# input = Variable(image_tensor)
	input = image_tensor.to(device)
	output = model(input)
	if device == 'cpu':
		index = output.data.cpu().numpy().argmax()
	else:
		index = output.data.cuda().numpy().argmax()


	print("ANSWER : ",classes[index],"[", index,"]" )

	APP_ID = '0818aa5a'
	APP_KEY = '9c558c2d5c3dffb5476c3be27f2aa197	'
	# food_item = 'cheese_plate'  # replace this to item from model
	food_item = classes[index]
	food_name1 = food_item.replace("_"," ")
	food_item = food_item.replace("_","+")
	base_url_ing = "https://api.edamam.com/search?q=" + food_item + "&app_id=" + APP_ID + "&app_key=" + APP_KEY
	item_details = requests.get(base_url_ing)
	item_details = item_details.json()
	print(item_details)
	recipes = item_details['hits'][0]['recipe']
	health_labels = recipes['healthLabels']         # categories
	ingredients_all = recipes['ingredientLines']    #ingredients with quantity
	calories = round(recipes['calories'],2)
	context = {"ingredients_all" : ingredients_all, 'item_name': food_item, 'health_label': health_labels, 'calories': calories}
	return HttpResponse(context)