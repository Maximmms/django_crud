from rest_framework import serializers

from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
	class Meta:
		model = StockProduct
		fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
	positions = ProductPositionSerializer(many = True)

	class Meta:
		model = Stock
		fields = ['address', 'positions']

	def create(self, validated_data):
		# достаем связанные данные для других таблиц
		positions = validated_data.pop('positions')

		# создаем склад по его параметрам
		stock = super().create(validated_data)

		# здесь вам надо заполнить связанные таблицы
		# в нашем случае: таблицу StockProduct
		# с помощью списка positions
		for position in positions:
			StockProduct.objects.create(stock = stock, **position)

		return stock

	def update(self, instance, validated_data):
		# достаем связанные данные для других таблиц
		positions = validated_data.pop('positions')

		# обновляем склад по его параметрам
		stock = super().update(instance, validated_data)

		# здесь вам надо обновить связанные таблицы
		# в нашем случае: таблицу StockProduct
		# с помощью списка positions
		if positions is not None:
			for position in positions:
				StockProduct.objects.create(stock = stock, **position)

		return stock