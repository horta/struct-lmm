import time
import sys
import os
import numpy as np
import pandas as pd
import scipy as sp
import h5py
import dask.dataframe as dd
from limix.data import BedReader
from limix.data import build_geno_query
from limix.data import GIter
from limix.util import unique_variants
from optparse import OptionParser
from struct_lmm import run_struct_lmm 
from struct_lmm.utils.sugar_utils import *

if __name__=='__main__':

    # define bed, phenotype and environment files
    bedfile = 'data_structlmm/chrom22_subsample20_maf0.10'
    phenofile = 'data_structlmm/expr.csv'
    envfile = 'data_structlmm/env.txt'

    # import geno and subset to first 1000 variants
    reader = BedReader(bedfile)
    query = build_geno_query(idx_start=0, idx_end=1000)
    reader.subset_snps(query, inplace=True)

    # pheno
    y = import_one_pheno_from_csv(phenofile,
                                  pheno_id='gene1.txt',
                                  standardize=True)

    # import environment
    E = sp.loadtxt(envfile)

    # mean as fixed effect 
    covs = sp.ones((E.shape[0], 1))

    # run analysis
    res = run_struct_lmm(reader, y, E,
                         covs=covs,
                         batch_size=100,
                         unique_variants=True)

    # export
    print 'Export to %s' % opt.ofile
    make_out_dir(opt.ofile)
    res.to_csv(opt.ofile, index=False)
