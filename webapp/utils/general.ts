// f)ormat n)umber with c)ommas
export const fnc = (number: number): string => {
	return new Intl.NumberFormat().format(number)
}
