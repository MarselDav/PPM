class PPM:
    def __init__(self, order, is_equally_probable=True, exclusion=False, update_exclusion=False):
        self.order = order
        self.symbols_cnt = 0  # число символов
        self.escape = b'\xff\xff'
        self.contexts = {}

        # методы улучшения сжатия
        self.update_exclusion = update_exclusion
        self.exclusion = exclusion

    def init_minus_one_context(self, symbols_set):
        self.contexts[-1] = {symbol: 1 for symbol in symbols_set}
        self.contexts[-1] = dict(sorted(self.contexts[-1].items()))

    @staticmethod
    def get_diffrent_symbols_cnt(data, data_len):
        symbols_set = set()
        diffrent_symbols_cnt = 0

        for i in range(data_len):
            symbol = data[i:i + 1]
            if symbol not in symbols_set:
                diffrent_symbols_cnt += 1
                symbols_set.add(symbol)
        return diffrent_symbols_cnt, symbols_set

    def update_contexts(self, context, symbol):
        if context not in self.contexts:
            self.contexts[context] = {}
        if symbol not in self.contexts[context]:
            self.contexts[context][symbol] = 0

            # Обновляем esc символ
            if self.escape not in self.contexts[context]:
                self.contexts[context][self.escape] = 0
            self.contexts[context][self.escape] += 1

            self.contexts[context] = dict(sorted(self.contexts[context].items()))

        self.contexts[context][symbol] += 1

    def update_model(self, context, last_context, symbol):
        for order in range(len(context) + 1):
            sub_context = context[order:]
            self.update_contexts(sub_context, symbol)

            if sub_context == last_context:
                break

    @staticmethod
    def get_cum_freq_under(context_dict, symbol):
        cum_freq_under = 0
        for s in context_dict.keys():
            if s == symbol:
                break

            cum_freq_under += context_dict[s]

        return cum_freq_under

    def get_probability(self, context, symbol, exclusion_symbols: set):
        if context in self.contexts:
            if len(exclusion_symbols) > 0:
                context_dict = {}

                for key in self.contexts[context]:
                    if key not in exclusion_symbols or key == self.escape:
                        context_dict[key] = self.contexts[context][key]
            else:
                context_dict = self.contexts[context]

            total_symbols = sum(context_dict.values()) - context_dict[self.escape]
            if symbol in context_dict:
                cum_freq_under = self.get_cum_freq_under(context_dict, symbol)
                # p(symbol) = c(s) / (c + d)
                return symbol, cum_freq_under, context_dict[symbol], total_symbols + context_dict[self.escape]

            else:  # такого символа нет в контексе, возвращаем esc
                # p(esc) = d / (d + c)
                return self.escape, total_symbols, context_dict[self.escape], total_symbols + \
                       context_dict[self.escape]

        return 0, 0, 0, 0  # потому что до этого такого контекста ещё не было, поэтому мы даже не возвращаем esc символ
