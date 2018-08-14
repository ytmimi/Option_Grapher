from rest_framework import serializers
from options.models import Option_Model

class Option_Serializer(serializers.ModelSerializer):
	class Meta:
		model = Option_Model
		fields = ('id', 'stock_ticker', 'quantity', 'position', 'option_type',
			'strike_price', 'stock_price', 'traded_price', 'interest_rate', 'days_till_exp')

	def create(self, validated_data):
		"""
		Create and return a new `Option_Model` instance, given the validated data.
		"""
		return Snippet.objects.create(**validated_data)

	def update(self, instance, validated_data):
		"""
		Update and return an existing `Option_Model` instance, given the validated data.
		"""
		instance.quantity = validated_data.get('quantity', instance.quantity)
		instance.position = validated_data.get('position', instance.position)
		instance.stock_price = validated_data.get('stock_price', instance.stock_price)
		instance.traded_price = validated_data.get('traded_price', instance.traded_price)
		instance.interest_rate = validated_data.get('interest_rate', instance.interest_rate)
		instance.days_till_exp = validated_data.get('days_till_exp', instance.days_till_exp)
		instance.save()
		return instance
