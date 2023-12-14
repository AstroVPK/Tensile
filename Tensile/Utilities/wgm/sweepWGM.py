import matplotlib.pyplot as plt
import argparse

import WGM


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--M", default=4096, type=int, help="M-dimensionof M x K x N GEMM")
    parser.add_argument("-n", "--N", default=4864, type=int, help="N-dimensionof M x K x N GEMM")
    parser.add_argument("-k", "--K", default=8192, type=int, help="K-dimensionof M x K x N GEMM")
    parser.add_argument("-mt0", "--MT0", default=128, type=int, help="M-dimensionof M x K x N GEMM")
    parser.add_argument("-mt1", "--MT1", default=128, type=int, help="N-dimensionof M x K x N GEMM")
    parser.add_argument("-du", "--DU", default=64, type=int, help="K-dimensionof M x K x N GEMM")
    parser.add_argument("-wl", "--wgm--low", dest='wgm_low', default=1, type=int, help="Work Group Mapping (WGM) low value")
    parser.add_argument("-wh", "--wgm--high", dest='wgm_high', default=304, type=int, help="Work Group Mapping (WGM) high value")
    parser.add_argument("-x", "--numXCDs", default=8, type=int, help="# of XCDs in GPU")
    parser.add_argument("-c", "--chunkSize", default=1, type=int, help="Chunksize used by GPU driver")
    parser.add_argument("--numCUsPerXCD", default=38, type=int, help="Number of CUs/XCD")
    parser.add_argument('--custom-wgm', dest='customWGM', action='store_true', help='Use the supplied custom WGM algorithm (default)ssssss')
    parser.add_argument('--no-custom-wgm', dest='customWGM', action='store_false', help='Use the standard WGM algorithm')
    parser.set_defaults(customWGM=True)
    args = parser.parse_args()

    for wgm in range(args.wgm_low, args.wgm_high+1):
        prob = WGM.Problem(args.M, args.N, args.K, wgm, WGM.gfx9(numXCDs=args.numXCDs, chunkSize=args.chunkSize, numCUsPerXCD=args.numCUsPerXCD), MT0=args.MT0, MT1=args.MT1, DU=args.DU, customWGM=args.customWGM)
        #prob.printWorkGroups()
        #prob.printNewWorkGroups()
        #prob.plotWorkGroups()
        #prob.plotNewWorkGroups(full_annotation=True)
        l2HitRate, mallHitRate, hbmHitRate = prob.getHitRates()
        print('wgm: %d; l2HitRate: %f; mallHitRate: %f; hbmHitRate: %f'%(wgm, l2HitRate, mallHitRate, hbmHitRate))
        #plt.show()
        #pdb.set_trace()