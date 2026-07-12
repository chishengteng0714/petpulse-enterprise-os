from modules.platform import render_platform


def main():
    """
    PetPulse Enterprise OS

    雲端部署啟動入口。
    僅負責啟動 PetPulse Enterprise OS，
    不修改任何 Runtime、Engine 或既有架構。
    """

    render_platform()


if __name__ == "__main__":
    main()