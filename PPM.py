class PPM:
    def __init__(self, order):
        self.order = order
        self.symbols_cnt = 0 # число символов
        self.escape = chr(257) + "ESC" + chr(257)
        self.contexts = {}

    def init_context(self, symbols_set):
        self.contexts[-1] = { symbol : 1  for symbol in symbols_set}

    @staticmethod
    def get_diffrent_symbols_cnt(data):
        symbols_set = set()
        diffrent_symbols_cnt = 0

        for symbol in data:
            if symbol not in symbols_set:
                diffrent_symbols_cnt += 1
                symbols_set.add(symbol)
        return diffrent_symbols_cnt, symbols_set

    def update_contexts(self, context, symbol):
        if context not in self.contexts:
            self.contexts[context] = {}
        if symbol not in self.contexts[context]:
            self.contexts[context][symbol] = 0

            # Обновляем максимально ебучий esc символ, который меня уже заебал
            if self.escape not in self.contexts[context]:
                self.contexts[context][self.escape] = 0
            self.contexts[context][self.escape] += 1

        self.contexts[context][symbol] += 1

    def update_model(self, context, symbol):
        for order in range(len(context) + 1):
            sub_context = context[order:]
            self.update_contexts(sub_context, symbol)

    @staticmethod
    def get_cum_freq_under(context_dict, symbol):
        cum_freq_under = 0
        for s in context_dict.keys():
            if s < symbol:
                cum_freq_under += context_dict[s]

        return cum_freq_under


    def get_probability(self, context, symbol):
        if context in self.contexts:
            # esc = len(self.contexts[context])
            total_symbols = sum(self.contexts[context].values())  - self.contexts[context][self.escape]
            if symbol in self.contexts[context]:
                cum_freq_under = self.get_cum_freq_under(self.contexts[context], symbol)
                # p(symbol) = c(s) / (c + d)
                # return cum_freq_under, self.contexts[context][symbol], total_symbols + esc
                return symbol, cum_freq_under, self.contexts[context][symbol], total_symbols + self.contexts[context][self.escape]

            else: # такого символа нет в контексе, возвращаем esc
                # p(esc) = d / (d + c)
                # print(f"symbol: {self.escape} :", total_symbols, esc, total_symbols + esc)
                # return total_symbols, esc, total_symbols + esc
                # print(f"symbol: {self.escape} :", total_symbols, self.contexts[context][self.escape], total_symbols + self.contexts[context][self.escape])
                return self.escape, total_symbols, self.contexts[context][self.escape], total_symbols + self.contexts[context][self.escape]

        return 0, 0, 0, 0 # потому что до этого такого контекста ещё не было, поэтому мы даже не возвращаем esc символ
