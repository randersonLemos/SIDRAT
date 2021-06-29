class GlobalPlotConfig:
    def __init__(self):
        self.figsize = (16, 9)
        self.title_fontsize = 20
        self.label_fontsize = 18
        self.legend_fontsize = 14
        self.suptitle_fontsize = 22
        self.tick_params_labelsize = 14

        self._config_figsize_16_9()


    def _config_figsize_16_9(self):
        if self.figsize == (16, 9):
            self.xsuptitle = 0.50
            self.ysuptitle = 0.98
            self.xlegend = 0.520
            self.ylegend = 0.0


