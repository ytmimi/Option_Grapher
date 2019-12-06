import datetime as dt
from rest_framework import serializers
from options.models import Option_Model, DATE_INPUTS

class Option_Serializer(serializers.ModelSerializer):
	expiration_date = serializers.DateField(format = DATE_INPUTS[0],
											input_formats = DATE_INPUTS)
	class Meta:
		model = Option_Model
		fields = ('__all__')

	def validate_stock_ticker(self, value):
		if type(value) == str:
			return value.upper()
		raise serializers.ValidationError(f'{value} must be of type String')

	def create(self, validated_data):
		"""
		Create and return a new `Option_Model` instance, given the validated data.
		"""
		option_model = Option_Model(**validated_data)
		option_model.set_days_till_expiration()
		option_model.save()
		return option_model

	def update(self, instance, validated_data):
		"""
		Update and return an existing `Option_Model` instance, given the validated data.
		"""
		instance.quantity = validated_data.get('quantity', instance.quantity)
		instance.position = validated_data.get('position', instance.position)
		instance.stock_price = validated_data.get('stock_price', instance.stock_price)
		instance.traded_price = validated_data.get('traded_price', instance.traded_price)
		instance.interest_rate = validated_data.get('interest_rate', instance.interest_rate)
		instance.days_till_exp = validated_data.get('expiration_date', instance.expiration_date)
		instance.set_days_till_expiration()
		instance.save()
		return instance
