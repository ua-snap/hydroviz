// f)ormat n)umber with c)ommas
export const fnc = number => {
	return new Intl.NumberFormat().format(number)
}
