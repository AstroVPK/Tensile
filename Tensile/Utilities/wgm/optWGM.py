import matplotlib.pyplot as plt
import argparse

import WGM


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--M', default=4096, type=int, help='M-dimensionof M x K x N GEMM')
    parser.add_argument('-n', '--N', default=4864, type=int, help='N-dimensionof M x K x N GEMM')
    parser.add_argument('-k', '--K', default=8192, type=int, help='K-dimensionof M x K x N GEMM')
    parser.add_argument('-mt0', '--MT0', default=128, type=int, help='M-dimensionof M x K x N GEMM')
    parser.add_argument('-mt1', '--MT1', default=128, type=int, help='N-dimensionof M x K x N GEMM')
    parser.add_argument('-wl', '--wgm--low', dest='wgm_low', default=1, type=int, help='Work Group Mapping (WGM) low value')
    parser.add_argument('-wh', '--wgm--high', dest='wgm_high', default=304, type=int, help='Work Group Mapping (WGM) high value')
    parser.add_argument('-x', '--numXCDs', default=8, type=int, help='# of XCDs in GPU')
    parser.add_argument('-c', '--chunkSize', default=1, type=int, help='Chunksize used by GPU driver')
    parser.add_argument('--numCUsPerXCD', default=38, type=int, help='Number of CUs/XCD')
    parser.add_argument('-opt-l2', '--optimize-l2-hit-rate', dest='opt_l2', action='store_true', help='Optimize WGM for the best L2 hit rate')
    parser.add_argument('-opt-mall', '--optimize-mall-hit-rate', dest='opt_mall', action='store_true', help='Optimize WGM for the best MALL hit rate')
    parser.add_argument('--custom-wgm', dest='customWGM', action='store_true', help='Use the supplied custom WGM algorithm (default)s')
    parser.add_argument('--no-custom-wgm', dest='customWGM', action='store_false', help='Use the standard WGM algorithm')
    parser.set_defaults(customWGM=True)
    parser.set_defaults(opt_l2=True)
    parser.set_defaults(opt_mall=False)
    parser.set_defaults(customWGM=True)
    args = parser.parse_args()

    l2HitRate_dict = dict()
    mallHitRate_dict = dict()
    hbmHitRate_dict = dict()
    for wgm in range(args.wgm_low, args.wgm_high+1):
        prob = WGM.Problem(args.M, args.N, args.K, wgm, WGM.gfx9(numXCDs=args.numXCDs, chunkSize=args.chunkSize, numCUsPerXCD=args.numCUsPerXCD), MT0=args.MT0, MT1=args.MT1, customWGM=args.customWGM)
        l2HitRate, mallHitRate, hbmHitRate = prob.getHitRates()
        l2HitRate_dict[wgm] = l2HitRate
        mallHitRate_dict[wgm] = mallHitRate
        hbmHitRate_dict[wgm] = hbmHitRate
    
    if args.opt_l2:
        max_wgm = max(l2HitRate_dict, key=l2HitRate_dict.get)
        max_l2HitRate = l2HitRate_dict[max_wgm]
        max_l2HitRate_mallHitRate = mallHitRate_dict[max_wgm]
        max_l2HitRate_hbmHitRate = hbmHitRate_dict[max_wgm]
        print('L2 Hit Rate is maximized for wgm: %d; l2HitRate: %f; mallHitRate: %f; hbmHitRate: %f'%(max_wgm, max_l2HitRate, max_l2HitRate_mallHitRate, max_l2HitRate_hbmHitRate))
    
    if args.opt_mall:
        max_wgm = max(mallHitRate_dict, key=mallHitRate_dict.get)
        max_mallHitRate = mallHitRate_dict[max_wgm]
        max_mallHitRate_l2HitRate = l2HitRate_dict[max_wgm]
        max_mallHitRate_hbmHitRate = hbmHitRate_dict[max_wgm]
        print('MALL Hit Rate is maximized for wgm: %d; l2HitRate: %f; mallHitRate: %f; hbmHitRate: %f'%(max_wgm, max_mallHitRate_l2HitRate, max_mallHitRate, max_mallHitRate_hbmHitRate))
