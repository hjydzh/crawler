#coding:utf-8

from jobUtils import fiveOneUtils
from common.DateUtils import DateUtils
from dao import jobService

def collection(date=DateUtils.day_now_str(DateUtils.STYLE_YMD)):
    driver = fiveOneUtils.get_firfox()
    job_details = []
    url = """
    http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=070200%2C00&district=000000&funtype=0000&industrytype=00&issuedate=9&providesalary=99&keyword=java&keywordtype=1&curr_page=1&lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=01&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&list_type=0&fromType=14&dibiaoid=-1
    """
    driver.get(url)
    detail = get_one_page_job(driver, None)
    jobService.insert_jobs(detail)
    job_details.extend(detail[5:])
    page = 2
    while True:
        date = '2015-11-06'
        url = """
    http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=070200%2C00&district=000000&funtype=0000&industrytype=00&issuedate=9&providesalary=99&keyword=java&keywordtype=1&curr_page=
    """ + str(page)
        url = url + '&lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=01&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&list_type=0&fromType=14&dibiaoid=-1'
        driver.get(url)
        details = get_one_page_job(driver, date)
        if details is None:
            break
        jobService.insert_jobs(details)
        #job_details.extend(detail)

        page = page + 1
    print ''

def get_one_page_job(driver,date):
    job_list = fiveOneUtils.get_job_list_url(driver)
    job_details = []
    for url in job_list:
        driver.get(url)
        try:
            job_detail = fiveOneUtils.get_job_detail(driver,date)
            if job_detail is None:
                return job_details
            print '%s %s %s %s %s %s %s %s' % (job_detail.company_name,job_detail.company_workers,job_detail.publish_date,job_detail.work_place,job_detail.experience_time,job_detail.diploma,job_detail.employ_nums,job_detail.job)
            job_details.append(job_detail)
        except Exception as e:
            pass
    return job_details
if __name__ == '__main__':
    collection()
