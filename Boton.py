class Boton():
	def __init__(self, imagen, pos, input_texto, fuente, color_base, color_hover):
		self.imagen = imagen
		self.posx = pos[0]
		self.posy = pos[1]
		self.fuente = fuente
		self.color_base = color_base
		self.color_hover = color_hover
		self.input_texto = input_texto
		self.texto = self.fuente.render(self.input_texto, True, self.color_base)
		if self.imagen is None:
			self.imagen = self.texto
		self.rect = self.imagen.get_rect(center = (self.posx,self.posy))
		self.texto_rect = self.texto.get_rect(center = (self.posx,self.posy))

	def actualizar(self, pantalla):
		if self.imagen is not None:
			pantalla.blit(self.imagen, self.rect)
		pantalla.blit(self.texto, self.texto_rect)

	def verificar_input(self, pos):
		retorno = False
		if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
			retorno = True
		return retorno

	def cambiar_color(self, pos):
		if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
			self.texto = self.fuente.render(self.input_texto, True, self.color_hover)
		else:
			self.texto = self.fuente.render(self.input_texto, True, self.color_base)